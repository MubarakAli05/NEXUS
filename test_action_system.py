from src.core.actions.system_actions import SystemActions

print("NEXUS ACTION SYSTEM TEST")
print("System info:", SystemActions.system_info())
print("Brightness:", SystemActions.get_brightness())
print("Volume:", SystemActions.get_volume())

# Uncomment one at a time when ready:
# SystemActions.take_screenshot()
# SystemActions.open_app("VS Code")
# SystemActions.close_app("VS Code")
# SystemActions.change_brightness(10)
# SystemActions.change_volume(10)
