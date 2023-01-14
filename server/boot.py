from lib.chronos import Chronos
from lib.wifi import MyWifi

import lib.file_utils as fu

MyWifi.autoconnect()

print("----- START BOOT -----")

print("    --> Chronos.sync() begin...")
Chronos.sync()
print("    --> %s" % (Chronos.now_str()))
print("    --> Chronos.sync() end.")

print("------ END BOOT ------")
