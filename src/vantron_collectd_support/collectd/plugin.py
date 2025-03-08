import collectd  # type: ignore

from .cpu_frequency import read_clock_frequency
from .power import read_power_consumption


def configure_plugin(event: collectd.Config, data: object | None = None):
    collectd.info("Setting up Vantron plugin")


collectd.register_config(configure_plugin)
collectd.register_read(read_clock_frequency)
collectd.register_read(read_power_consumption)
