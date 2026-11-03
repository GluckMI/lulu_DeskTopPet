import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from lulu_pet.assets import AssetManager
from lulu_pet.characters import spec_by_id
from lulu_pet.controller import PetController
from lulu_pet.models import PetSettings
from lulu_pet.motion import MotionMode
from lulu_pet.pet_window import PetWindow
from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent


class FakeMouseEvent:
    def __init__(self, button):
        self._button = button
        self.accepted = False

    def button(self):
        return self._button

    def accept(self):
        self.accepted = True


class FakeBubble:
    def __init__(self):
        self.messages = []

    def show_message(self, text, anchor, duration_ms=2600):
        self.messages.append(text)

    def hide(self):
        pass


def double_click_event() -> QMouseEvent:
    point = QPointF(20, 20)
    return QMouseEvent(
        QEvent.MouseButtonDblClick,
        point,
        point,
        Qt.LeftButton,
        Qt.LeftButton,
        Qt.NoModifier,
    )


class PetWindowStickerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_trigger_sticker_plays_inside_pet_window_not_popup(self):
        settings = PetSettings(
            window_size=(220, 180),
            always_on_top=True,
            speech_interval_seconds=45,
            edge_snap=True,
            autostart=False,
            motion_speed_percent=100,
        )
        window = PetWindow(PetController(AssetManager(None)), settings)
        try:
            window.trigger_sticker()

            self.assertTrue(window._sticker_active)
            self.assertFalse(window._sticker.isVisible())
        finally:
            window.close()

    def test_trigger_sticker_uses_character_matching_gif_library(self):
        settings = PetSettings(
            window_size=(220, 180),
            always_on_top=True,
            speech_interval_seconds=45,
            edge_snap=True,
            autostart=False,
            motion_speed_percent=100,
        )
        window = PetWindow(PetController(AssetManager(None)), settings)
        try:
            # 默认呆猫形象：双击播放呆猫自己的动态 GIF
            window.trigger_sticker()
            self.assertIsNotNone(window._last_sticker_path)
            self.assertEqual(window._last_sticker_path.parent, spec_by_id("batiao").dir_path)
            self.assertTrue(window._sticker_movie.frameCount() > 1)

            # 切到噜噜形象后：双击走噜噜素材池
            window.select_character(spec_by_id("lulu"))
            window.trigger_sticker()
            self.assertEqual(window._last_sticker_path.parent, spec_by_id("lulu").dir_path)
        finally:
            window.close()

    def test_trigger_sticker_always_stays_inside_current_character_pool(self):
        settings = PetSettings(
            window_size=(220, 180),
            always_on_top=True,
            speech_interval_seconds=45,
            edge_snap=True,
            autostart=False,
            motion_speed_percent=100,
        )
        window = PetWindow(PetController(AssetManager(None)), settings)
        try:
            batiao_pool = set(spec_by_id("batiao").all_gifs())
            for _ in range(10):
                window.trigger_sticker()
                self.assertIn(window._last_sticker_path, batiao_pool)

            window.select_character(spec_by_id("lulu"))
            lulu_pool = set(spec_by_id("lulu").all_gifs())
            for _ in range(10):
                window.trigger_sticker()
                self.assertIn(window._last_sticker_path, lulu_pool)
        finally:
            window.close()

    def test_sticker_playback_freezes_pet_position_until_finished(self):
        settings = PetSettings(
            window_size=(220, 180),
            always_on_top=True,
            speech_interval_seconds=45,
            edge_snap=True,
            autostart=False,
            motion_speed_percent=100,
        )
        window = PetWindow(PetController(AssetManager(None)), settings)
        try:
            window.motion.start(MotionMode.WALK_RIGHT, duration_ticks=20)
            start = (window.motion.x, window.motion.y)

            window.trigger_sticker()
            for _ in range(4):
                window._on_tick()
            during_sticker = (window.motion.x, window.motion.y)
            window._clear_sticker()
            window._on_tick()
            after_sticker = (window.motion.x, window.motion.y)

            self.assertEqual(during_sticker, start)
            self.assertNotEqual(after_sticker, start)
        finally:
            window.close()

    def test_single_click_does_not_trigger_sticker(self):
        settings = PetSettings(
            window_size=(220, 180),
            always_on_top=True,
            speech_interval_seconds=45,
            edge_snap=True,
            autostart=False,
            motion_speed_percent=100,
        )
        window = PetWindow(PetController(AssetManager(None)), settings)
        event = FakeMouseEvent(Qt.LeftButton)
        try:
            window.mouseReleaseEvent(event)

            self.assertTrue(event.accepted)
            self.assertFalse(window._sticker_active)
        finally:
            window.close()

    def test_single_click_does_not_show_bubble(self):
        settings = PetSettings(
            window_size=(220, 180),
            always_on_top=True,
            speech_interval_seconds=45,
            edge_snap=True,
            autostart=False,
            motion_speed_percent=100,
        )
        window = PetWindow(PetController(AssetManager(None)), settings)
        event = FakeMouseEvent(Qt.LeftButton)
        bubble = FakeBubble()
        window._bubble = bubble
        try:
            window.mouseReleaseEvent(event)

            self.assertTrue(event.accepted)
            self.assertEqual(bubble.messages, [])
        finally:
            window.close()

    def test_double_click_triggers_sticker(self):
        settings = PetSettings(
            window_size=(220, 180),
            always_on_top=True,
            speech_interval_seconds=45,
            edge_snap=True,
            autostart=False,
            motion_speed_percent=100,
        )
        window = PetWindow(PetController(AssetManager(None)), settings)
        event = double_click_event()
        try:
            window.mouseDoubleClickEvent(event)

            self.assertTrue(event.isAccepted())
            self.assertTrue(window._sticker_active)
        finally:
            window.close()

    def test_double_click_shows_bubble(self):
        settings = PetSettings(
            window_size=(220, 180),
            always_on_top=True,
            speech_interval_seconds=45,
            edge_snap=True,
            autostart=False,
            motion_speed_percent=100,
        )
        window = PetWindow(PetController(AssetManager(None)), settings)
        event = double_click_event()
        bubble = FakeBubble()
        window._bubble = bubble
        try:
            window.mouseDoubleClickEvent(event)

            self.assertTrue(event.isAccepted())
            self.assertEqual(len(bubble.messages), 1)
            self.assertTrue(bubble.messages[0])
        finally:
            window.close()

    def test_trigger_sticker_plays_more_slowly_than_default_movie_speed(self):
        settings = PetSettings(
            window_size=(220, 180),
            always_on_top=True,
            speech_interval_seconds=45,
            edge_snap=True,
            autostart=False,
            motion_speed_percent=100,
        )
        window = PetWindow(PetController(AssetManager(None)), settings)
        try:
            window.trigger_sticker()

            self.assertIsNotNone(window._sticker_movie)
            self.assertLess(window._sticker_movie.speed(), 100)
        finally:
            window.close()

    def test_sticker_uses_whole_character_folder_as_pool(self):
        settings = PetSettings(
            window_size=(220, 180),
            always_on_top=True,
            speech_interval_seconds=45,
            edge_snap=True,
            autostart=False,
            motion_speed_percent=100,
        )
        window = PetWindow(PetController(AssetManager(None)), settings)
        try:
            # 双击表情包的可选范围就是当前形象目录里的全部 GIF
            self.assertEqual(
                set(window._spec.all_gifs()),
                set(spec_by_id("batiao").all_gifs()),
            )
            self.assertEqual(len(window._spec.all_gifs()), 9)
        finally:
            window.close()


if __name__ == "__main__":
    unittest.main()
