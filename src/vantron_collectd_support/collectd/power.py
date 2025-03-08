import math
import re
import subprocess
import time
from dataclasses import dataclass
from typing import Dict, List

import collectd  # type: ignore
from loguru import logger

from vantron_collectd_support.util import _nn_

SAMPLE_PARSE_PATTERN = re.compile(
    r"""^\s*
        (?P<sys>[0-9A-Z_]+)_[VA]
        \s
        (?P<unit>current|volt)
        \(
        (?P<id>\d+)
        \)=
        (?P<value>\d+\.\d+)
        [AV]\s*$""",
    re.VERBOSE | re.MULTILINE,
)


@dataclass
class VoltageCurrentSystemSample:
    name: str
    voltage_v: float | None = None
    current_a: float | None = None

    @property
    def is_missing_reading(self) -> bool:
        return self.voltage_v is None or self.current_a is None

    @property
    def power_w(self) -> float:
        if self.is_missing_reading:
            raise AttributeError(f".power_w requires .voltage_v and .current_a to be non-null, name={self.name}")
        return _nn_(self.voltage_v) * _nn_(self.current_a)


def read_power_consumption(data=None):
    """Read power consumption and push it to collectd."""
    ts = math.floor(time.time())
    samples = parse_vcgencmd_output(call_vcgencmd())
    power_consumed_w = compute_power_consumption(samples)

    values = collectd.Values(type="gauge", plugin="power_use")
    values.dispatch(time=ts, values=[power_consumed_w])


def call_vcgencmd():
    """Call the vcgencmd command to read power metrics."""
    try:
        cmd_out = str(subprocess.check_output(args=["vcgencmd", "pmic_read_adc"], encoding="utf8"))
    except:
        logger.exception("Failed to read")
        raise
    return cmd_out


def parse_vcgencmd_output(cmd_out: str) -> List[VoltageCurrentSystemSample]:
    """Parse the output of the vcgencmd command."""
    sample_map: Dict[str, VoltageCurrentSystemSample] = {}
    for m in [_nn_(SAMPLE_PARSE_PATTERN.match(line)) for line in cmd_out.splitlines()]:
        name, unit, value = m["sys"], m["unit"], float(m["value"])
        sample = sample_map.setdefault(name, VoltageCurrentSystemSample(name=name))
        if unit == "volt":
            sample.voltage_v = value
        elif unit == "current":
            sample.current_a = value
        else:
            raise ValueError(f"{unit} is not a valid unit")

    return [s for s in sample_map.values() if not s.is_missing_reading]


def compute_power_consumption(samples: List[VoltageCurrentSystemSample]) -> float:
    """Compute power consumption from voltage and current samples."""
    measured_power = sum(s.power_w for s in samples)
    # The PMIC does not report all power consumption, however, it has been
    # found that it can be used to approximate the total consumption.
    # https://github.com/jfikar/RPi5-power
    adjusted_power = measured_power * 1.1451 + 0.5879

    return adjusted_power
