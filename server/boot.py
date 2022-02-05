from lib.chronos import Chronos
import lib.file_utils as fu

print("----- START BOOT -----")

print("    --> Chronos.sync() begin...")
Chronos.sync()
print("    --> %s" % (Chronos.now_str()))
print("    --> Chronos.sync() end.")

print("------ END BOOT ------")
