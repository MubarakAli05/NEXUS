"""
NEXUS Windows System Actions
============================

This module contains computer-control primitives only.
Intent recognition, AI, memory, UI and voice belong elsewhere.

The implementation is deliberately Windows-focused because NEXUS is
currently being developed for a Windows laptop.

Dependencies are optional where practical. If a dependency is missing,
the individual feature returns False/None instead of crashing NEXUS.
"""

from __future__ import annotations

import ctypes
import os
import shutil
import subprocess
import time
import webbrowser
from pathlib import Path
from typing import Any, Optional


# Optional packages
try:
    import pyautogui
except ImportError:
    pyautogui = None

try:
    import psutil
except ImportError:
    psutil = None

try:
    import screen_brightness_control as sbc
except ImportError:
    sbc = None

try:
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from comtypes import CLSCTX_ALL
except ImportError:
    AudioUtilities = None
    IAudioEndpointVolume = None
    CLSCTX_ALL = None


class SystemActions:
    """Low-level actions NEXUS can request on Windows."""

    APP_ALIASES = {
        "vs code": "code",
        "visual studio code": "code",
        "vscode": "code",
        "blender": "blender",
        "notepad": "notepad",
        "calculator": "calc",
        "calc": "calc",
        "paint": "mspaint",
        "file explorer": "explorer",
        "explorer": "explorer",
        "command prompt": "cmd",
        "cmd": "cmd",
        "powershell": "powershell",
        "task manager": "taskmgr",
        "control panel": "control",
        "settings": "ms-settings:",
        "snipping tool": "snippingtool",
    }

    PROCESS_ALIASES = {
        "vs code": "Code.exe",
        "visual studio code": "Code.exe",
        "vscode": "Code.exe",
        "blender": "blender.exe",
        "notepad": "notepad.exe",
        "paint": "mspaint.exe",
        "calculator": "CalculatorApp.exe",
    }

    SPECIAL_FOLDERS = {
        "desktop": Path.home() / "Desktop",
        "documents": Path.home() / "Documents",
        "downloads": Path.home() / "Downloads",
        "pictures": Path.home() / "Pictures",
        "music": Path.home() / "Music",
        "videos": Path.home() / "Videos",
    }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _clean(value: Any) -> str:
        if value is None:
            return ""
        value = str(value).lower().strip()
        return " ".join(value.strip(" .,!?;:'\"").split())

    @staticmethod
    def _run(command, *, timeout=20, shell=False):
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=shell,
        )

    @staticmethod
    def _powershell(command: str, *, timeout=20):
        return SystemActions._run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                command,
            ],
            timeout=timeout,
        )

    @staticmethod
    def _key(key: str) -> bool:
        if pyautogui is None:
            print("❌ pyautogui is not installed.")
            return False
        try:
            pyautogui.press(key)
            return True
        except Exception as exc:
            print(f"❌ Keyboard action failed: {exc}")
            return False

    @staticmethod
    def _hotkey(*keys: str) -> bool:
        if pyautogui is None:
            print("❌ pyautogui is not installed.")
            return False
        try:
            pyautogui.hotkey(*keys)
            return True
        except Exception as exc:
            print(f"❌ Hotkey failed: {exc}")
            return False

    # ------------------------------------------------------------------
    # Power / session
    # ------------------------------------------------------------------

    @staticmethod
    def lock_system() -> bool:
        print("🔒 NEXUS: Locking system...")
        return bool(ctypes.windll.user32.LockWorkStation())

    @staticmethod
    def shutdown(delay: int = 0) -> bool:
        print("⏻ NEXUS: Shutting down...")
        subprocess.Popen(["shutdown", "/s", "/t", str(max(0, int(delay)))])
        return True

    @staticmethod
    def restart(delay: int = 0) -> bool:
        print("🔄 NEXUS: Restarting...")
        subprocess.Popen(["shutdown", "/r", "/t", str(max(0, int(delay)))])
        return True

    @staticmethod
    def cancel_shutdown() -> bool:
        result = SystemActions._run(["shutdown", "/a"])
        return result.returncode == 0

    @staticmethod
    def sleep() -> bool:
        print("😴 NEXUS: Sleeping...")
        result = SystemActions._powershell(
            "Add-Type -AssemblyName System.Windows.Forms; "
            "[System.Windows.Forms.Application]::SetSuspendState('Suspend',$false,$false)"
        )
        return result.returncode == 0

    @staticmethod
    def hibernate() -> bool:
        print("💤 NEXUS: Hibernating...")
        result = SystemActions._run(["shutdown", "/h"])
        return result.returncode == 0

    @staticmethod
    def sign_out() -> bool:
        print("🚪 NEXUS: Signing out...")
        subprocess.Popen(["shutdown", "/l"])
        return True

    # ------------------------------------------------------------------
    # Applications / windows
    # ------------------------------------------------------------------

    @staticmethod
    def open_app(app_name: str) -> bool:
        name = SystemActions._clean(app_name)
        command = SystemActions.APP_ALIASES.get(name, name)
        if not command:
            return False

        print(f"🚀 NEXUS: Opening {app_name}...")
        try:
            if command.endswith(":"):
                os.startfile(command)
            else:
                subprocess.Popen(command, shell=True)
            return True
        except Exception as exc:
            print(f"❌ Open failed: {exc}")
            return False

    @staticmethod
    def close_app(app_name: str) -> bool:
        name = SystemActions._clean(app_name)
        process = SystemActions.PROCESS_ALIASES.get(name)

        if not process:
            print(f"❌ NEXUS: Unknown application: {app_name}")
            return False

        print(f"🛑 NEXUS: Closing {app_name}...")
        try:
            result = SystemActions._run(["taskkill", "/IM", process, "/F"])
            return result.returncode == 0
        except Exception as exc:
            print(f"❌ Close failed: {exc}")
            return False

    @staticmethod
    def minimize_active_window() -> bool:
        return SystemActions._hotkey("win", "down")

    @staticmethod
    def maximize_active_window() -> bool:
        return SystemActions._hotkey("win", "up")

    @staticmethod
    def close_active_window() -> bool:
        return SystemActions._hotkey("alt", "f4")

    @staticmethod
    def switch_window() -> bool:
        return SystemActions._hotkey("alt", "tab")

    @staticmethod
    def show_desktop() -> bool:
        return SystemActions._hotkey("win", "d")

    @staticmethod
    def open_task_manager() -> bool:
        return SystemActions.open_app("task manager")

    # ------------------------------------------------------------------
    # Screenshots / screen
    # ------------------------------------------------------------------

    @staticmethod
    def take_screenshot(directory="data/screenshots") -> str | bool:
        if pyautogui is None:
            print("❌ pyautogui is not installed.")
            return False

        folder = Path(directory)
        folder.mkdir(parents=True, exist_ok=True)
        filename = f"screenshot_{time.strftime('%Y%m%d_%H%M%S')}.png"
        path = folder / filename

        try:
            pyautogui.screenshot().save(path)
            print(f"📸 NEXUS: Screenshot saved to {path}")
            return str(path)
        except Exception as exc:
            print(f"❌ Screenshot failed: {exc}")
            return False

    @staticmethod
    def set_brightness(value: int) -> bool:
        if sbc is None:
            print("❌ screen-brightness-control is not installed.")
            return False
        try:
            value = max(0, min(100, int(value)))
            sbc.set_brightness(value)
            print(f"☀️ NEXUS: Brightness set to {value}%.")
            return True
        except Exception as exc:
            print(f"❌ Brightness failed: {exc}")
            return False

    @staticmethod
    def get_brightness() -> Optional[int]:
        if sbc is None:
            return None
        try:
            values = sbc.get_brightness()
            return values[0] if isinstance(values, list) else int(values)
        except Exception as exc:
            print(f"❌ Brightness read failed: {exc}")
            return None

    @staticmethod
    def brightness_up(step: int = 10) -> bool:
        current = SystemActions.get_brightness()
        return False if current is None else SystemActions.set_brightness(current + step)

    @staticmethod
    def brightness_down(step: int = 10) -> bool:
        current = SystemActions.get_brightness()
        return False if current is None else SystemActions.set_brightness(current - step)

    @staticmethod
    def night_light(on: bool = True) -> bool:
        # Windows night-light API is not consistently exposed as a simple
        # command. This opens the relevant settings page reliably.
        try:
            os.startfile("ms-settings:nightlight")
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Audio
    # ------------------------------------------------------------------

    @staticmethod
    def _volume_endpoint():
        if AudioUtilities is None:
            return None
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None,
        )
        return interface.QueryInterface(IAudioEndpointVolume)

    @staticmethod
    def get_volume() -> Optional[int]:
        try:
            endpoint = SystemActions._volume_endpoint()
            if endpoint is None:
                return None
            return round(endpoint.GetMasterVolumeLevelScalar() * 100)
        except Exception as exc:
            print(f"❌ Volume read failed: {exc}")
            return None

    @staticmethod
    def set_volume(value: int) -> bool:
        try:
            endpoint = SystemActions._volume_endpoint()
            if endpoint is None:
                return False
            value = max(0, min(100, int(value)))
            endpoint.SetMasterVolumeLevelScalar(value / 100.0, None)
            print(f"🔊 NEXUS: Volume set to {value}%.")
            return True
        except Exception as exc:
            print(f"❌ Volume failed: {exc}")
            return False

    @staticmethod
    def volume_up(step: int = 10) -> bool:
        current = SystemActions.get_volume()
        return False if current is None else SystemActions.set_volume(current + step)

    @staticmethod
    def volume_down(step: int = 10) -> bool:
        current = SystemActions.get_volume()
        return False if current is None else SystemActions.set_volume(current - step)

    @staticmethod
    def mute() -> bool:
        try:
            endpoint = SystemActions._volume_endpoint()
            if endpoint is None:
                return False
            endpoint.SetMute(1, None)
            print("🔇 NEXUS: Muted.")
            return True
        except Exception as exc:
            print(f"❌ Mute failed: {exc}")
            return False

    @staticmethod
    def unmute() -> bool:
        try:
            endpoint = SystemActions._volume_endpoint()
            if endpoint is None:
                return False
            endpoint.SetMute(0, None)
            print("🔊 NEXUS: Unmuted.")
            return True
        except Exception as exc:
            print(f"❌ Unmute failed: {exc}")
            return False

    @staticmethod
    def play_pause() -> bool:
        return SystemActions._key("playpause")

    @staticmethod
    def next_track() -> bool:
        return SystemActions._key("nexttrack")

    @staticmethod
    def previous_track() -> bool:
        return SystemActions._key("prevtrack")

    # ------------------------------------------------------------------
    # Keyboard / mouse
    # ------------------------------------------------------------------

    @staticmethod
    def type_text(text: str) -> bool:
        if pyautogui is None:
            return False
        try:
            pyautogui.write(str(text), interval=0.01)
            return True
        except Exception as exc:
            print(f"❌ Typing failed: {exc}")
            return False

    @staticmethod
    def press_key(key: str) -> bool:
        return SystemActions._key(SystemActions._clean(key))

    @staticmethod
    def hotkey(*keys: str) -> bool:
        return SystemActions._hotkey(*keys)

    @staticmethod
    def move_mouse(x: int, y: int) -> bool:
        if pyautogui is None:
            return False
        try:
            pyautogui.moveTo(int(x), int(y), duration=0.15)
            return True
        except Exception as exc:
            print(f"❌ Mouse move failed: {exc}")
            return False

    @staticmethod
    def click_mouse(button="left") -> bool:
        if pyautogui is None:
            return False
        try:
            pyautogui.click(button=button)
            return True
        except Exception as exc:
            print(f"❌ Mouse click failed: {exc}")
            return False

    @staticmethod
    def double_click() -> bool:
        if pyautogui is None:
            return False
        try:
            pyautogui.doubleClick()
            return True
        except Exception as exc:
            print(f"❌ Double-click failed: {exc}")
            return False

    @staticmethod
    def right_click() -> bool:
        return SystemActions.click_mouse("right")

    @staticmethod
    def scroll(amount: int) -> bool:
        if pyautogui is None:
            return False
        try:
            pyautogui.scroll(int(amount))
            return True
        except Exception as exc:
            print(f"❌ Scroll failed: {exc}")
            return False

    # ------------------------------------------------------------------
    # Clipboard
    # ------------------------------------------------------------------

    @staticmethod
    def copy() -> bool:
        return SystemActions._hotkey("ctrl", "c")

    @staticmethod
    def paste() -> bool:
        return SystemActions._hotkey("ctrl", "v")

    @staticmethod
    def cut() -> bool:
        return SystemActions._hotkey("ctrl", "x")

    @staticmethod
    def undo() -> bool:
        return SystemActions._hotkey("ctrl", "z")

    @staticmethod
    def redo() -> bool:
        return SystemActions._hotkey("ctrl", "y")

    @staticmethod
    def select_all() -> bool:
        return SystemActions._hotkey("ctrl", "a")

    # ------------------------------------------------------------------
    # Files / folders
    # ------------------------------------------------------------------

    @staticmethod
    def open_path(path: str) -> bool:
        try:
            resolved = Path(path).expanduser()
            if not resolved.exists():
                print(f"❌ Path not found: {path}")
                return False
            os.startfile(str(resolved))
            return True
        except Exception as exc:
            print(f"❌ Open path failed: {exc}")
            return False

    @staticmethod
    def open_special_folder(name: str) -> bool:
        key = SystemActions._clean(name)
        path = SystemActions.SPECIAL_FOLDERS.get(key)
        return False if path is None else SystemActions.open_path(str(path))

    @staticmethod
    def create_folder(path: str) -> bool:
        try:
            Path(path).expanduser().mkdir(parents=True, exist_ok=True)
            return True
        except Exception as exc:
            print(f"❌ Create folder failed: {exc}")
            return False

    @staticmethod
    def rename_path(source: str, destination: str) -> bool:
        try:
            Path(source).expanduser().rename(Path(destination).expanduser())
            return True
        except Exception as exc:
            print(f"❌ Rename failed: {exc}")
            return False

    @staticmethod
    def copy_path(source: str, destination: str) -> bool:
        try:
            src = Path(source).expanduser()
            dst = Path(destination).expanduser()
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            return True
        except Exception as exc:
            print(f"❌ Copy failed: {exc}")
            return False

    @staticmethod
    def move_path(source: str, destination: str) -> bool:
        try:
            shutil.move(str(Path(source).expanduser()), str(Path(destination).expanduser()))
            return True
        except Exception as exc:
            print(f"❌ Move failed: {exc}")
            return False

    @staticmethod
    def delete_path(path: str, permanent: bool = False) -> bool:
        """Delete a file/folder.

        `permanent=False` is intentionally conservative: it refuses to
        perform a destructive deletion here. The final NEXUS confirmation
        layer should decide when deletion is allowed.
        """
        if not permanent:
            print("⚠️ Delete requested but confirmation/permanent=True was not supplied.")
            return False

        try:
            p = Path(path).expanduser()
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
            return True
        except Exception as exc:
            print(f"❌ Delete failed: {exc}")
            return False

    # ------------------------------------------------------------------
    # Network / Windows settings
    # ------------------------------------------------------------------

    @staticmethod
    def open_settings(page: str = "") -> bool:
        try:
            uri = "ms-settings:" + str(page).strip()
            os.startfile(uri)
            return True
        except Exception as exc:
            print(f"❌ Settings failed: {exc}")
            return False

    @staticmethod
    def wifi_settings() -> bool:
        return SystemActions.open_settings("network-wifi")

    @staticmethod
    def bluetooth_settings() -> bool:
        return SystemActions.open_settings("bluetooth")

    @staticmethod
    def display_settings() -> bool:
        return SystemActions.open_settings("display")

    @staticmethod
    def sound_settings() -> bool:
        return SystemActions.open_settings("sound")

    @staticmethod
    def network_info() -> dict:
        result = SystemActions._run(
            ["ipconfig", "/all"],
            timeout=10,
        )
        return {
            "returncode": result.returncode,
            "output": result.stdout,
            "error": result.stderr,
        }

    @staticmethod
    def toggle_wifi() -> bool:
        # Uses Windows netsh. Adapter names can differ; if "Wi-Fi" does not
        # exist on a machine, the command will fail safely.
        result = SystemActions._run(
            ["netsh", "interface", "set", "interface", "name=Wi-Fi", "admin=disabled"]
        )
        return result.returncode == 0

    # ------------------------------------------------------------------
    # Monitoring
    # ------------------------------------------------------------------

    @staticmethod
    def system_info() -> dict:
        if psutil is None:
            return {}

        try:
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage(Path.home().anchor)
            battery = psutil.sensors_battery()

            return {
                "cpu_percent": psutil.cpu_percent(interval=0.5),
                "memory_percent": mem.percent,
                "memory_used_gb": round(mem.used / 1024**3, 2),
                "memory_available_gb": round(mem.available / 1024**3, 2),
                "disk_percent": disk.percent,
                "disk_free_gb": round(disk.free / 1024**3, 2),
                "battery_percent": None if battery is None else battery.percent,
                "charging": None if battery is None else battery.power_plugged,
            }
        except Exception as exc:
            print(f"❌ System info failed: {exc}")
            return {}

    @staticmethod
    def cpu_usage() -> Optional[float]:
        if psutil is None:
            return None
        return psutil.cpu_percent(interval=0.5)

    @staticmethod
    def ram_usage() -> Optional[float]:
        if psutil is None:
            return None
        return psutil.virtual_memory().percent

    @staticmethod
    def disk_usage() -> Optional[float]:
        if psutil is None:
            return None
        return psutil.disk_usage(Path.home().anchor).percent

    @staticmethod
    def battery_status() -> dict:
        if psutil is None:
            return {}
        battery = psutil.sensors_battery()
        if battery is None:
            return {}
        return {
            "percent": battery.percent,
            "charging": battery.power_plugged,
            "seconds_left": battery.secsleft,
        }

    # ------------------------------------------------------------------
    # Web / utility launchers
    # ------------------------------------------------------------------

    @staticmethod
    def open_url(url: str) -> bool:
        try:
            webbrowser.open(str(url))
            return True
        except Exception as exc:
            print(f"❌ URL open failed: {exc}")
            return False

    @staticmethod
    def open_browser() -> bool:
        try:
            webbrowser.open("about:blank")
            return True
        except Exception:
            return False
