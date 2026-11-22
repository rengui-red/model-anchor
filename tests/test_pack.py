"""最小测试：三种模式、过期检测、关键词过滤、profile 渲染。"""
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "packer"))

from modes import build_full, build_minimal, build_task_scoped, _filter_by_keyword
from stale import check_stale


class TestModes(unittest.TestCase):
    def setUp(self):
        self.anchor = "# 断点\n\n## 当前\n改 cookie\n\n## 下一步\n写回退\n\n## 阻塞\n无\n"

    def test_minimal_contains_anchor(self):
        out = build_minimal(self.anchor, "generic")
        self.assertIn("改 cookie", out)
        self.assertIn("写回退", out)

    def test_full_without_instructions_falls_back(self):
        out = build_full(self.anchor, "", "generic")
        self.assertIn("改 cookie", out)

    def test_full_with_instructions(self):
        out = build_full(self.anchor, "## 技术栈\nPython", "generic")
        self.assertIn("Python", out)
        self.assertIn("改 cookie", out)

    def test_task_scoped_filters(self):
        instr = "## 认证\ncookie 逻辑\n\n## 数据库\nSQL"
        out = build_task_scoped(self.anchor, instr, "cookie", "generic")
        self.assertIn("cookie", out)
        self.assertNotIn("SQL", out)

    def test_filter_empty_keyword_returns_all(self):
        instr = "## 认证\ncookie\n\n## 数据库\nSQL"
        self.assertEqual(_filter_by_keyword(instr, ""), instr)


class TestStale(unittest.TestCase):
    def test_fresh_file_no_warning(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "断点.md"
            f.write_text("x", encoding="utf-8")
            check_stale(Path(d), "断点.md")  # 不应抛异常

    def test_stale_file_detected(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "断点.md"
            f.write_text("x", encoding="utf-8")
            old = time.time() - 48 * 3600
            os.utime(f, (old, old))
            check_stale(Path(d), "断点.md")  # 打印提醒，不抛异常


class TestProfiles(unittest.TestCase):
    def test_list_profiles_contains_known(self):
        from profiles import list_profiles
        names = list_profiles()
        for expected in ("generic", "claude", "deepseek", "doubao"):
            self.assertIn(expected, names)

    def test_unknown_profile_falls_back(self):
        from profiles import load_profile
        text = load_profile("nonexistent-model")
        self.assertTrue(text.strip())
        self.assertIn("{{anchor}}", text)

    def test_render_replaces_placeholder(self):
        from profiles import render
        out = render("前\n{{anchor}}\n后", "断点内容")
        self.assertIn("断点内容", out)
        self.assertNotIn("{{anchor}}", out)

    def test_render_with_instructions(self):
        from profiles import render
        out = render("{{anchor}}", "断点", "项目指令")
        self.assertIn("项目指令", out)
        self.assertIn("断点", out)

    def test_model_specific_wording(self):
        from modes import build_minimal
        claude_out = build_minimal("断点内容", "claude")
        deepseek_out = build_minimal("断点内容", "deepseek")
        generic_out = build_minimal("断点内容", "generic")
        self.assertNotEqual(claude_out, deepseek_out)
        self.assertNotEqual(claude_out, generic_out)
        self.assertIn("断点内容", claude_out)
        self.assertIn("断点内容", deepseek_out)


if __name__ == "__main__":
    unittest.main()



