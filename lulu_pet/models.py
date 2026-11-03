from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PetSettings:
    window_size: tuple[int, int]
    always_on_top: bool
    speech_interval_seconds: int
    edge_snap: bool
    autostart: bool
    motion_speed_percent: int = 100
    contract_name: str = "shouting"
    # 双击表情包播放速度（百分比，越小越慢）
    sticker_playback_percent: int = 50
    # 日常动作 GIF 播放速度（百分比，越小越慢）
    character_playback_percent: int = 70
    # 待机随机换图间隔（秒）
    idle_switch_interval_seconds: int = 8


@dataclass(frozen=True)
class PetAction:
    name: str
    file_path: Path | None
    file_paths: tuple[Path, ...]
    duration_ms: int
    weight: int
    lines: tuple[str, ...]
