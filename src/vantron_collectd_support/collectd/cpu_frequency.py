import math
import time

import collectd  # type: ignore

SYSTEM_CLOCK_FREQUENCY_PATH = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"


def read_clock_frequency(data=None):
    with open(SYSTEM_CLOCK_FREQUENCY_PATH, "r") as f:
        ts = math.floor(time.time())
        cpu_frequency = int(f.readline())
    collectd.debug(f"Reading CPU clock frequency, {cpu_frequency / 1000000.0:.2f} Ghz")

    values = collectd.Values(type="cpufreq", plugin="cpu")
    values.dispatch(time=ts, values=[cpu_frequency])
