from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QSpinBox,
    QVBoxLayout,
)

from .models import PetSettings


class SettingsDialog(QDialog):
    def __init__(self, settings: PetSettings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("噜噜设置")
        self.setModal(True)

        self.speed = QSpinBox(self)
        self.speed.setRange(40, 220)
        self.speed.setSuffix("%")
        self.speed.setSingleStep(10)
        self.speed.setValue(settings.motion_speed_percent)

        self.speech_interval = QSpinBox(self)
        self.speech_interval.setRange(10, 300)
        self.speech_interval.setSuffix(" 秒")
        self.speech_interval.setSingleStep(5)
        self.speech_interval.setValue(settings.speech_interval_seconds)

        self.sticker_speed = QSpinBox(self)
        self.sticker_speed.setRange(20, 100)
        self.sticker_speed.setSuffix("%")
        self.sticker_speed.setSingleStep(5)
        self.sticker_speed.setValue(settings.sticker_playback_percent)

        self.character_speed = QSpinBox(self)
        self.character_speed.setRange(20, 100)
        self.character_speed.setSuffix("%")
        self.character_speed.setSingleStep(5)
        self.character_speed.setValue(settings.character_playback_percent)

        self.idle_interval = QSpinBox(self)
        self.idle_interval.setRange(3, 60)
        self.idle_interval.setSuffix(" 秒")
        self.idle_interval.setSingleStep(1)
        self.idle_interval.setValue(settings.idle_switch_interval_seconds)

        self.always_on_top = QCheckBox(self)
        self.always_on_top.setChecked(settings.always_on_top)

        self.edge_snap = QCheckBox(self)
        self.edge_snap.setChecked(settings.edge_snap)

        form = QFormLayout()
        form.addRow("移动速度", self.speed)
        form.addRow("说话间隔", self.speech_interval)
        form.addRow("双击表情速度", self.sticker_speed)
        form.addRow("动作播放速度", self.character_speed)
        form.addRow("待机换图间隔", self.idle_interval)
        form.addRow("保持置顶", self.always_on_top)
        form.addRow("边缘限制", self.edge_snap)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def to_settings(self, current: PetSettings) -> PetSettings:
        return PetSettings(
            window_size=current.window_size,
            always_on_top=self.always_on_top.isChecked(),
            speech_interval_seconds=self.speech_interval.value(),
            edge_snap=self.edge_snap.isChecked(),
            autostart=current.autostart,
            motion_speed_percent=self.speed.value(),
            contract_name=current.contract_name,
            sticker_playback_percent=self.sticker_speed.value(),
            character_playback_percent=self.character_speed.value(),
            idle_switch_interval_seconds=self.idle_interval.value(),
        )
