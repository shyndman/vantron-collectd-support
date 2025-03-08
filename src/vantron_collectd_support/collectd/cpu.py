import math
import time

import collectd  # type: ignore

_SYSTEM_CPU_CLOCK_FREQUENCY_PATH = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"
_SYSTEM_CPU_FAN_SPEED_PATH = "/sys/devices/platform/cooling_fan/hwmon/hwmon3/fan1_input"


def read_cpu_metrics(data=None):
    """Read CPU metrics and push them to collectd."""
    _push_fan_speed()
    _push_clock_frequency()


def _push_fan_speed():
    """Push CPU fan speed to collectd."""
    with open(_SYSTEM_CPU_FAN_SPEED_PATH, "r") as f:
        ts = math.floor(time.time())
        fan_speed = int(f.readline())
    collectd.debug(f"Reading CPU fan speed, {fan_speed} Hz")

    values = collectd.Values(type="fanspeed", plugin="cpu")
    values.dispatch(time=ts, values=[fan_speed])


def _push_clock_frequency():
    """Push CPU clock frequency to collectd."""
    with open(_SYSTEM_CPU_CLOCK_FREQUENCY_PATH, "r") as f:
        ts = math.floor(time.time())
        cpu_frequency = int(f.readline())
    collectd.debug(f"Reading CPU clock frequency, {cpu_frequency / 1000000.0:.2f} Ghz")

    values = collectd.Values(type="cpufreq", plugin="cpu")
    values.dispatch(time=ts, values=[cpu_frequency])
