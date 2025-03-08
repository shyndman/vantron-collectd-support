import math
import time

import collectd  # type: ignore

SYSTEM_CLOCK_FREQUENCY_PATH = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"


def read_clock_frequency(data=None):
    """
    Reads the current CPU clock frequency and dispatches it as a collectd value.
    
    This function opens the system file defined by SYSTEM_CLOCK_FREQUENCY_PATH, reads the CPU frequency in hertz from its first line, and logs the frequency in megahertz. It then creates a collectd.Values object with the type "cpufreq" and plugin "cpu", dispatching the read value along with the current timestamp. The optional 'data' parameter is currently not used.
    """
    with open(SYSTEM_CLOCK_FREQUENCY_PATH, "r") as f:
        ts = math.floor(time.time())
        cpu_frequency = int(f.readline())
    collectd.debug(f"Reading CPU clock frequency, {cpu_frequency / 1000000.0:.2f} Mhz")

    values = collectd.Values(type="cpufreq", plugin="cpu")
    values.dispatch(time=ts, values=[cpu_frequency])
