# NEXUS actions-only package

Copy/merge the `src/core/actions` files into the existing NEXUS project.

This package contains the action layer only:
- system power
- applications
- screenshots
- brightness
- volume/audio
- media
- keyboard shortcuts
- files/folders
- Wi-Fi/Bluetooth helpers
- system/battery/network information
- Windows utilities

It intentionally does not replace the existing IntentEngine, VoiceAssistant, UI, AI, memory, or main.py.

Before using actions, install:
    pip install -r requirements-actions.txt

Shutdown/restart/sleep/hibernate and file deletion are real actions.
Test them individually before exposing them to voice commands.
