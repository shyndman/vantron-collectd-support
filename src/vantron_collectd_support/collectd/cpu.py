import math
import time

import collectd  # type: ignore

_SYSTEM_CPU_CLOCK_FREQUENCY_PATH = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"
_SYSTEM_CPU_FAN_SPEED_PATH = "/sys/devices/platform/cooling_fan/hwmon/hwmon3/fan1_input"


def read_cpu_metrics(data=None):
    """
    Reads and dispatches CPU metrics via Collectd.
    
    This function triggers the collection of CPU fan speed and clock frequency metrics by
    calling internal helper functions. The optional 'data' parameter is provided to conform
    to the expected interface but is currently not used.
    """
    _push_fan_speed()
    _push_clock_frequency()


def _push_fan_speed():
    """
    Reads and dispatches the CPU fan speed metric.
    
    Opens the system file to obtain the fan speed in hertz, logs the value for debugging, and dispatches the metric to
    Collectd with the current timestamp using the 'cpu' plugin.
    """
    with open(_SYSTEM_CPU_FAN_SPEED_PATH, "r") as f:
        ts = math.floor(time.time())
        fan_speed = int(f.readline())
    collectd.debug(f"Reading CPU fan speed, {fan_speed} Hz")

    values = collectd.Values(type="fanspeed", plugin="cpu")
    values.dispatch(time=ts, values=[fan_speed])


def _push_clock_frequency():
    """
    Reads the CPU clock frequency and dispatches it to Collectd.
    
    Opens the system file containing the CPU clock frequency, converts the value to an
    integer, and logs the frequency in gigahertz. Dispatches the frequency metric along
    with the current timestamp via Collectd.
    """
    with open(_SYSTEM_CPU_CLOCK_FREQUENCY_PATH, "r") as f:
        ts = math.floor(time.time())
        cpu_frequency = int(f.readline())
    collectd.debug(f"Reading CPU clock frequency, {cpu_frequency / 1000000.0:.2f} Ghz")

    values = collectd.Values(type="cpufreq", plugin="cpu")
    values.dispatch(time=ts, values=[cpu_frequency])
