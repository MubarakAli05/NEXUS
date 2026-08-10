from src.core.intent.intents import IntentType
from src.core.actions.system_actions import SystemActions


class ActionEngine:
    """Maps IntentType values to SystemActions.

    Your existing IntentType enum can be expanded later. This engine uses
    enum names for optional actions so the project does not crash merely
    because an optional intent has not been added yet.
    """

    def __init__(self):
        self.system = SystemActions()

    def execute(self, intent):
        intent_type = intent.type
        name = getattr(intent_type, "name", "")
        target = getattr(intent, "target", None)
        value = getattr(intent, "value", None)

        if intent_type == IntentType.LOCK_SYSTEM:
            return self.system.lock_system()

        if intent_type == IntentType.OPEN_APP:
            return self.system.open_app(target)

        if intent_type == IntentType.CLOSE_APP:
            return self.system.close_app(target)

        if intent_type == IntentType.TAKE_SCREENSHOT:
            return self.system.take_screenshot()

        handlers = {
            "SHUTDOWN": self.system.shutdown,
            "RESTART": self.system.restart,
            "SLEEP": self.system.sleep,
            "HIBERNATE": self.system.hibernate,
            "SIGN_OUT": self.system.sign_out,
            "CANCEL_SHUTDOWN": self.system.cancel_shutdown,

            "BRIGHTNESS_UP": self.system.brightness_up,
            "BRIGHTNESS_DOWN": self.system.brightness_down,
            "SET_BRIGHTNESS": lambda: self.system.set_brightness(value),

            "VOLUME_UP": self.system.volume_up,
            "VOLUME_DOWN": self.system.volume_down,
            "SET_VOLUME": lambda: self.system.set_volume(value),
            "MUTE": self.system.mute,
            "UNMUTE": self.system.unmute,

            "PLAY_PAUSE": self.system.play_pause,
            "NEXT_TRACK": self.system.next_track,
            "PREVIOUS_TRACK": self.system.previous_track,

            "MINIMIZE_WINDOW": self.system.minimize_active_window,
            "MAXIMIZE_WINDOW": self.system.maximize_active_window,
            "CLOSE_WINDOW": self.system.close_active_window,
            "SWITCH_WINDOW": self.system.switch_window,
            "SHOW_DESKTOP": self.system.show_desktop,

            "SYSTEM_INFO": self.system.system_info,
            "CPU_USAGE": self.system.cpu_usage,
            "RAM_USAGE": self.system.ram_usage,
            "DISK_USAGE": self.system.disk_usage,
            "BATTERY_STATUS": self.system.battery_status,
            "NETWORK_INFO": self.system.network_info,

            "WIFI_SETTINGS": self.system.wifi_settings,
            "BLUETOOTH_SETTINGS": self.system.bluetooth_settings,
            "DISPLAY_SETTINGS": self.system.display_settings,
            "SOUND_SETTINGS": self.system.sound_settings,

            "PLAY_PAUSE_MEDIA": self.system.play_pause,
        }

        handler = handlers.get(name)

        if handler:
            return handler()

        print(f"⚠️ NEXUS: No action handler for {intent_type}")
        return False
