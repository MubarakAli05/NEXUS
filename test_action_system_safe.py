from src.core.actions.system_actions import SystemActions

print("======================================")
print("      NEXUS ACTION SAFE TEST")
print("======================================")

print("System info:")
print(SystemActions.system_info())

print()
print("Brightness:")
print(SystemActions.get_brightness())

print()
print("Volume:")
print(SystemActions.get_volume())

print()
print("Battery:")
print(SystemActions.battery_status())

print()
print("Safe action layer import: OK")
print("======================================")
