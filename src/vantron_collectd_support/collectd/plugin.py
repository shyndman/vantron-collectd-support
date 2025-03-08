import collectd  # type: ignore

from .cpu_frequency import read_clock_frequency

collectd.register_read(read_clock_frequency)
