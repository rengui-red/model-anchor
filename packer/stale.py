"""断点过期检测。仅提醒，不阻断。"""
import sys
import time
from pathlib import Path

STALE_HOURS = 24


def check_stale(project_path: Path, anchor_file: str,
                threshold_hours: float = STALE_HOURS) -> None:
    anchor = project_path / anchor_file
    if not anchor.exists():
        return
    age_hours = (time.time() - anchor.stat().st_mtime) / 3600
    if age_hours > threshold_hours:
        print(
            f"[提醒] {anchor_file} 已 {age_hours:.0f} 小时未更新，"
            f"建议让 AI 刷新或手动确认。",
            file=sys.stderr,
        )




