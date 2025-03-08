import collectd  # type: ignore

from .cpu import read_cpu_metrics
from .power import read_power_consumption


def configure_plugin(event: collectd.Config, data: object | None = None):
    """
    Configure the Vantron plugin for Collectd.
    
    This callback is invoked during the configuration phase by Collectd.
    It logs an informational message to indicate that the Vantron plugin is being set up.
    
    Args:
        event: The Collectd configuration event.
        data: Optional additional data (unused).
    """
    collectd.info("Setting up Vantron plugin")


collectd.register_config(configure_plugin)
collectd.register_read(read_cpu_metrics)
collectd.register_read(read_power_consumption)
