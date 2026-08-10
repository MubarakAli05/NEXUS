# NEXUS — Actions Only

This folder is the Windows computer-control layer for NEXUS.

Included action families:
- Power/session: lock, shutdown, restart, sleep, hibernate, sign out
- Applications: open/close common apps
- Windows: minimize, maximize, close, switch, show desktop, task manager
- Display: screenshot, brightness, display settings, night-light settings
- Audio: volume, mute, media playback controls, sound settings
- Keyboard/mouse: type, keys, hotkeys, click, double-click, right-click, scroll
- Clipboard/editing: copy, paste, cut, undo, redo, select all
- Files/folders: open, create, rename, copy, move, guarded delete
- Connectivity/settings: Wi-Fi/Bluetooth/display/sound settings, network info
- Monitoring: CPU, RAM, disk, battery, general system information
- Web: open URL/browser

This is intentionally an ACTION package, not the complete NEXUS application.

IMPORTANT:
1. Add the listed optional IntentType members to your existing enum.
2. Add matching natural-language rules/AI mappings in IntentEngine.
3. Add confirmation rules in the final NEXUS core before destructive actions.
4. Test each action independently before enabling voice control.

Some actions are machine-specific (brightness, Wi-Fi adapter names, media keys).
The implementation returns False/None when the required capability is unavailable.
