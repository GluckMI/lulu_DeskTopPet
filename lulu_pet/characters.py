from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .paths import resource_path

# 所有形象素材统一放在 assets/characters/<folder>/
CHARACTERS_ASSET_PARTS = ("assets", "characters")


@dataclass(frozen=True)
class CharacterSpec:
    """一个可选用的桌宠形象。后续扩展只需新增一个 CharacterSpec 并放入对应素材目录。"""

    character_id: str
    label: str
    folder: str
    # 素材本体是否需要按朝向水平翻转（噜噜本体朝左、向右时翻转；呆猫方向图已自带朝向）
    mirror_facing: bool
    # 移动/翻滚时使用的无方向本体文件名；呆猫用专门的左右跑图，可留空
    move_body: str | None = None
    lifted: str | None = None
    rest: str | None = None
    run_right: str | None = None
    run_left: str | None = None
    # 待机随机池需要排除的文件名（如呆猫的左右跑图）
    idle_exclude: tuple[str, ...] = ()

    @property
    def dir_path(self) -> Path:
        return resource_path(*CHARACTERS_ASSET_PARTS, self.folder)

    def all_gifs(self) -> list[Path]:
        return sorted(self.dir_path.glob("*.gif"))

    def idle_pool(self) -> list[Path]:
        return [path for path in self.all_gifs() if path.name not in self.idle_exclude]

    def slot_path(self, filename: str | None) -> Path | None:
        if not filename:
            return None
        return self.dir_path / filename


CHARACTER_SPECS: tuple[CharacterSpec, ...] = (
    CharacterSpec(
        character_id="batiao",
        label="呆猫八条",
        folder="batiao",
        mirror_facing=False,
        lifted="cat_jump.gif",
        rest="cat_fail.gif",
        run_right="cat_run_right.gif",
        run_left="cat_run_left.gif",
        idle_exclude=("cat_run_right.gif", "cat_run_left.gif"),
    ),
    CharacterSpec(
        character_id="lulu",
        label="噜噜",
        folder="lulu",
        mirror_facing=True,
        move_body="lulu_transparent_09.gif",
        lifted="xhs_lulu_01.gif",
        rest="qq_lulu_04.gif",
    ),
)

DEFAULT_SPEC = CHARACTER_SPECS[0]


def spec_by_id(character_id: str) -> CharacterSpec:
    for spec in CHARACTER_SPECS:
        if spec.character_id == character_id:
            return spec
    raise KeyError(character_id)
