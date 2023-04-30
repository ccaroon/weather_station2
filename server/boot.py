from lib.chronos import Chronos
from lib.wifi import MyWifi
from secrets import SECRETS

import lib.file_utils as fu

MyWifi.autoconnect()
Chronos.sync(tz_offset=SECRETS["tz_offset"])
