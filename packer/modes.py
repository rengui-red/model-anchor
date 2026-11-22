"""三种打包模式。minimal/full 走 profile 渲染；task-scoped 先过滤再走 profile。"""
import re

from profiles import load_profile, render


def build_minimal(anchor_text: str, model: str = "generic") -> str:
    template = load_profile(model)
    return render(template, anchor_text)


def build_full(anchor_text: str, instructions: str, model: str = "generic") -> str:
    template = load_profile(model)
    return render(template, anchor_text, instructions)


def _filter_by_keyword(text: str, keyword: str) -> str:
    """保留包含关键词的行，及其所属的 ## 标题行。"""
    if not keyword.strip():
        return text
    kw = keyword.lower()
    out, keep_section = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            keep_section = kw in line.lower()
            if keep_section:
                out.append(line)
            continue
        if keep_section or kw in line.lower():
            out.append(line)
    return "\n".join(out).strip()


def build_task_scoped(anchor_text: str, instructions: str, task: str,
                      model: str = "generic") -> str:
    filtered = _filter_by_keyword(instructions, task)
    header = f"当前聚焦任务：{task}\n\n"
    scoped = header
    if filtered:
        scoped += filtered + "\n\n"
    scoped += anchor_text
    template = load_profile(model)
    return render(template, scoped)



