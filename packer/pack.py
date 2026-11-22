#!/usr/bin/env python3
"""ModelAnchor packer v0.1 — 断点 → 接续 prompt。仅标准库。"""
import argparse
import shutil
import sys
from pathlib import Path

from modes import build_full, build_minimal, build_task_scoped
from profiles import list_profiles
from stale import check_stale

ANCHOR_FILE = "断点.md"


def load_anchor(project_path: Path) -> str:
    """读取断点。未来云端/MCP 版本只替换此函数体，打包逻辑不动。"""
    anchor = project_path / ANCHOR_FILE
    if not anchor.exists():
        sys.exit(f"未找到 {anchor}，请先运行: python pack.py --init")
    return anchor.read_text(encoding="utf-8")


def load_project_instructions(project_path: Path) -> str:
    for name in ("CLAUDE.md", "AGENTS.md"):
        f = project_path / name
        if f.exists():
            return f.read_text(encoding="utf-8")
    return ""


def init_template(project_path: Path) -> None:
    src = Path(__file__).resolve().parent.parent / "templates" / ANCHOR_FILE
    dst = project_path / ANCHOR_FILE
    if dst.exists():
        sys.exit(f"{dst} 已存在，不覆盖。")
    shutil.copy(src, dst)
    print(f"已生成 {dst}，请填写四个字段。")


def main() -> None:
    parser = argparse.ArgumentParser(description="ModelAnchor packer v0.1")
    parser.add_argument("--init", action="store_true", help="生成断点模板")
    parser.add_argument("--minimal", action="store_true", help="极简打包模式")
    parser.add_argument("--full", action="store_true", help="完整打包模式")
    parser.add_argument("--task", default="", help="task-scoped 关键词")
    parser.add_argument("--model", default="generic",
                        help=f"目标模型 profile，可用: {', '.join(list_profiles())}")
    parser.add_argument("--project", default=".", help="项目路径")
    parser.add_argument("--no-stale-check", action="store_true", help="跳过过期检测")
    args = parser.parse_args()

    project_path = Path(args.project).resolve()

    if args.init:
        init_template(project_path)
        return

    if not args.no_stale_check:
        check_stale(project_path, ANCHOR_FILE)

    anchor_text = load_anchor(project_path)

    if args.task:
        instructions = load_project_instructions(project_path)
        print(build_task_scoped(anchor_text, instructions, args.task, args.model))
    elif args.full:
        instructions = load_project_instructions(project_path)
        print(build_full(anchor_text, instructions, args.model))
    else:
        print(build_minimal(anchor_text, args.model))


if __name__ == "__main__":
    main()




