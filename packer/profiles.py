"""model profile 加载与渲染。纯字符串替换，不做任何模型 API 调用。"""
import sys
from pathlib import Path

PROFILE_DIR = Path(__file__).resolve().parent / "profiles"
PLACEHOLDER = "{{anchor}}"


def list_profiles() -> list[str]:
    return sorted(p.stem for p in PROFILE_DIR.glob("*.md"))


def load_profile(name: str) -> str:
    """加载 profile 模板。未知模型名回退到 generic。"""
    path = PROFILE_DIR / f"{name}.md"
    if not path.exists():
        print(
            f"[提醒] 未找到 profile '{name}'，回退到 generic。"
            f"可用: {', '.join(list_profiles())}",
            file=sys.stderr,
        )
        path = PROFILE_DIR / "generic.md"
    return path.read_text(encoding="utf-8")


def render(template: str, anchor_text: str, instructions: str = "") -> str:
    """把断点和（可选）项目指令填入模板占位符。"""
    body = anchor_text
    if instructions.strip():
        body = (
            "以下是项目常驻指令，整个会话必须遵守：\n\n"
            f"{instructions}\n\n---\n\n"
            "以下是当前断点：\n\n"
            f"{anchor_text}"
        )
    if PLACEHOLDER not in template:
        return template.rstrip() + "\n\n" + body + "\n"
    return template.replace(PLACEHOLDER, body)




