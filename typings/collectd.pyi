from collections.abc import Sequence
from typing import List, Protocol, Self, Tuple

class CollectdError(Exception):
    """Basic exception for collectd Python scripts.

    Throwing this exception will not cause a stacktrace to be logged, even if LogTraces is enabled in the config.
    """

    pass

class Signed(int):
    pass

class Unsigned(int):
    pass

class Config:
    parent: Self | None
    key: str
    values: Tuple[str, ...]
    children: List[Self]

class PluginData:
    host: str
    plugin: str
    plugin_instance: str
    time: int
    type: str
    type_instance: str

class Values(PluginData):
    interval: int | None
    values: Sequence[int | float] | None
    meta: dict[str, int | float | bool | str]

    def __init__(
        self,
        host: str | None = None,
        plugin: str | None = None,
        plugin_instance: str | None = None,
        time: int | None = None,
        type: str | None = None,
        type_instance: str | None = None,
        interval: int | None = None,
        values: Sequence[int | float] | None = None,
    ):
        """
        Initialises a new Values instance.
        
        Sets up a plugin data object with optional attributes for host, plugin, plugin
        instance, event time, data type, and type instance, as well as the collection
        interval and measurement values.
        """
        pass

    def dispatch(
        self,
        type: str | None = None,
        values: Sequence[int | float] | None = None,
        plugin_instance: str | None = None,
        type_instance: str | None = None,
        plugin: str | None = None,
        host: str | None = None,
        time: int | None = None,
        interval: int | None = None,
    ) -> None:
        """Dispatch plugin data.
        
        Dispatches collected plugin data to the monitoring system with optional metadata
        overrides. Use the parameters to specify measurement details such as metric type,
        value sequence, plugin instance, type instance, plugin name, host, timestamp, and
        update interval.
        
        Parameters:
            type (str, optional): Metric category or identifier.
            values (Sequence[int | float], optional): Numeric measurement values.
            plugin_instance (str, optional): Identifier for the specific plugin instance.
            type_instance (str, optional): Further classification for the metric.
            plugin (str, optional): Plugin name override.
            host (str, optional): Originating host of the data.
            time (int, optional): Timestamp associated with the data.
            interval (int, optional): Interval in seconds between consecutive measurements.
        """
        pass

    def write(
        self,
        destination: str | None = None,
        type: str | None = None,
        values: Sequence[int | float] | None = None,
        plugin_instance: str | None = None,
        type_instance: str | None = None,
        plugin: str | None = None,
        host: str | None = None,
        time: int | None = None,
        interval: int | None = None,
    ) -> None:
        """
        Writes plugin data to a specified destination.
        
        This method writes the collected plugin data, using either the instance's
        stored values or those provided via keyword arguments, to the specified
        destination. Optional parameters allow for overriding default attributes
        such as the plugin name, host, and timing information.
        
        Parameters:
            destination: The target for data submission, if different from the default.
            type: The data type descriptor that categorises the information.
            values: A sequence of integers or floats representing the data.
            plugin_instance: An identifier for a particular plugin instance.
            type_instance: An identifier for a specific type instance.
            plugin: An override for the plugin name.
            host: An override for the originating host.
            time: The Unix timestamp at which the data was collected.
            interval: The interval between data collections.
        """
        pass

class Notification(PluginData):
    def __init__(
        self,
        host: str | None = None,
        plugin: str | None = None,
        plugin_instance: str | None = None,
        time: int | None = None,
        type: str | None = None,
        type_instance: str | None = None,
    ):
        """
        Initialises a PluginData instance.
        
        Optional plugin attributes are provided to describe the data, including the host name,
        plugin name, plugin instance identifier, timestamp (in seconds since epoch), type, and
        type instance. All parameters default to None if not specified.
        """
        pass

class Callback[EventT](Protocol):
    def __call__(self, event: EventT, data: object | None) -> None:
        """
        Invokes the callback with the given event and supplementary data.
        
        Args:
            event: The event instance to be processed.
            data: Optional additional information related to the event.
        """
        pass

class LogCallback[EventT](Protocol):
    def __call__(self, severity: int, message: str, data: object | None) -> None:
        """
        Log a message with a given severity and optional supplementary data.
        
        Args:
            severity (int): The log message's severity level.
            message (str): The content of the log message.
            data (object | None): Optional additional information to include with the log.
        """
        pass

class FlushCallback[EventT](Protocol):
    def __call__(self, timeout: int, id: str | None, data: object | None) -> None:
        """Invoke the flush callback.
        
        Processes a flush event using the provided timeout. An optional identifier and
        additional data can be supplied to customise the flush operation.
        
        Args:
            timeout: The duration for the flush operation.
            id: An optional identifier for the flush event.
            data: Supplementary data to be used during the flush process.
        """
        pass

class NoEventCallback(Protocol):
    def __call__(self, data: object | None) -> None:
        """Invoke the instance as a callable with an optional data argument.
        
        This method enables the instance to be used as a callback. An optional data value
        can be supplied to provide additional context during invocation.
        
        Args:
            data: Optional data to be used during the callback call.
        """
        pass

type CallbackIdentifier = str

def unregister_log(identifier: CallbackIdentifier) -> None:
    """
    Unregisters a log callback.
    
    Removes the log callback associated with the provided identifier from the registry, ensuring that it will no longer receive log events.
    
    Args:
        identifier: A unique callback identifier returned by register_log.
    """
    pass

def register_log(callback: LogCallback, data: object | None = None, name: str | None = None) -> CallbackIdentifier:
    """
    Registers a log callback.
    
    Registers the provided logging callback with an optional data argument and an optional
    name. The callback will be invoked for logging events, and the function returns a unique
    identifier that can be used to unregister the callback.
      
    Args:
        callback: The logging callback to handle log events.
        data: Optional data passed to the callback during invocation.
        name: Optional name for identifying the callback.
      
    Returns:
        A unique identifier for the registered callback.
    """
    pass

def unregister_config(identifier: CallbackIdentifier) -> None:
    """
    Unregisters a configuration callback.
    
    Removes the configuration callback associated with the specified identifier.
    """
    pass

def register_config(callback: Callback[Config], data: object = None, name: str | None = None) -> CallbackIdentifier:
    """
    Registers a callback for configuration events.
    
    This function adds a callback that is invoked when configuration updates occur, passing a Config object to the callback. Optional data and a custom name can be provided for additional context.
    
    Args:
        callback: A callable that processes configuration events represented by a Config instance.
        data: Optional extra data to associate with the callback.
        name: Optional name to identify the callback.
    
    Returns:
        A unique identifier for the registered configuration callback.
    """
    pass

def unregister_init(identifier: CallbackIdentifier) -> None:
    """
    Unregisters an initialization callback.
    
    Removes a previously registered callback for initialization events using its unique
    identifier.
    """
    pass

def register_init(callback: NoEventCallback, data: object = None, name: str | None = None) -> CallbackIdentifier:
    """
    Registers an initialisation callback.
    
    This function registers a callback that is executed during the initialisation phase.
    The callback receives no event information. Optional data and a name can be provided
    to associate additional context with the callback. The function returns an identifier
    that can be used to unregister the callback.
    """
    pass

def unregister_read(identifier: CallbackIdentifier) -> None:
    """Unregisters a read callback using its identifier.
    
    Args:
        identifier: The callback identifier returned by `register_read` that uniquely
            identifies the read callback to be unregistered.
    """
    pass

def register_read(
    callback: NoEventCallback, interval_s: float = 0, data: object = None, name: str | None = None
) -> CallbackIdentifier:
    """
    Registers a read callback for periodic execution.
    
    This function registers a callback to be invoked on read events. If a positive
    interval is specified via interval_s, the callback is scheduled to execute every
    interval_s seconds. The callback, which receives no event data, may use the provided
    data for custom processing, and an optional name can be assigned for easier
    identification. A unique callback identifier is returned for later unregistration.
        
    Args:
        callback: A callable to be executed on read events.
        interval_s: Interval in seconds between invocations; defaults to 0.
        data: Optional additional data passed to the callback.
        name: Optional identifier for the callback.
        
    Returns:
        CallbackIdentifier: A unique identifier for the registered callback.
    """
    pass

def unregister_write(identifier: CallbackIdentifier) -> None:
    """
    Unregister the write callback.
    
    Removes the write callback associated with the provided identifier, ensuring it is not invoked in future operations.
    
    Args:
        identifier: The unique identifier for the registered write callback.
    """
    pass

def register_write(callback: Callback[Values], data: object = None, name: str | None = None) -> CallbackIdentifier:
    """
    Registers a write callback for handling plugin data.
    
    This function registers a callback designed for processing write operations on
    plugin data (Values) and returns a unique identifier for the registration.
    Optional context data and a callback name may be provided.
        
    Args:
        callback: The callback function that processes write operations for plugin data.
        data: Optional context data passed to the callback.
        name: An optional name used to identify the callback.
    
    Returns:
        A unique identifier for the registered callback.
    """
    pass

def unregister_notification(identifier: CallbackIdentifier) -> None:
    """
    Unregisters a notification callback.
    
    Removes the notification callback associated with the provided callback
    identifier, ensuring that it will not be invoked for future notifications.
    """
    pass

def register_notification(
    callback: Callback[Notification], data: object = None, name: str | None = None
) -> CallbackIdentifier:
    """
    Registers a notification callback.
    
    Associates a callback function to handle notification events, optionally including additional data or a name for identification. Returns a unique identifier for the registered callback.
    
    Args:
        callback: The function to invoke when a notification event occurs.
        data: Optional extra data to pass to the callback.
        name: An optional label for the callback registration.
    
    Returns:
        A unique identifier corresponding to the registered callback.
    """
    pass

def unregister_flush(identifier: CallbackIdentifier) -> None:
    """
    Unregisters a flush callback using its identifier.
    
    Removes the flush callback registered via register_flush so that it is no longer invoked during flush events.
    """
    pass

def register_flush(callback: FlushCallback, data: object = None, name: str | None = None) -> CallbackIdentifier:
    """
    Registers a flush callback.
    
    Registers a callback function to handle flush events with optional context data
    and a human-readable name. Returns a unique identifier for the registered flush callback.
    """
    pass

def unregister_shutdown(identifier: CallbackIdentifier) -> None:
    """
    Unregisters a shutdown callback.
    
    Removes the shutdown callback associated with the provided identifier.
    """
    pass

def register_shutdown(callback: NoEventCallback, data: object = None, name: str | None = None) -> CallbackIdentifier:
    """
    Registers a shutdown callback for handling shutdown events.
    
    This function registers a callback to be executed during the shutdown phase, allowing custom routines to run as the system terminates. Optional additional data can be passed to the callback, and an optional name may be provided for identification purposes.
    
    Args:
        callback: A callable invoked on shutdown.
        data: Optional extra data passed to the callback.
        name: Optional identifier for the callback.
    
    Returns:
        A unique identifier for the registered shutdown callback.
    """
    pass

def get_dataset(name: str) -> List[Tuple[str, str, float | None, float | None]]:
    """
    Retrieves a dataset by name.
    
    Given the name of a dataset, this function returns a list of tuples that specify
    the data source details. Each tuple contains two strings (the data source name
    and type descriptor) followed by two optional floats representing the minimum
    and maximum values, respectively.
    
    Args:
        name: The name of the dataset to retrieve.
    
    Returns:
        A list of tuples, where each tuple includes:
            - A string for the data source name.
            - A string for the data source type.
            - A float for the minimum value, or None if not applicable.
            - A float for the maximum value, or None if not applicable.
    """
    pass

def flush(plugin: str, timeout: int | None = -1, identifier: str | None = None):
    """
    Flushes pending data for the specified plugin.
    
    Triggers a flush of buffered data for the given plugin. An optional timeout
    can be provided to limit the flush duration, and an optional identifier can be
    used to distinguish this flush request from others.
    
    Args:
        plugin: The name of the plugin whose data should be flushed.
        timeout: An optional timeout in seconds; use -1 to indicate the default flush behaviour.
        identifier: An optional identifier to uniquely tag the flush request.
    """
    pass

def error(msg: str):
    """
    Logs an error message.
    
    Args:
        msg: The error message to log.
    """
    pass

def warning(msg: str):
    """
    Logs a warning message.
    
    This function records a warning-level message. The message should describe a potential issue 
    or unexpected behaviour that does not necessarily halt execution.
    """
    pass

def notice(msg: str):
    """Log a notice-level message.
    
    Records an informational notice message to highlight significant events that
    require notice-level attention, but are not as severe as warnings.
    
    Args:
        msg: The message text to log.
    """
    pass

def info(msg: str):
    """
    Logs an informational message.
    
    Args:
        msg: The message to be logged.
    """
    pass

def debug(msg: str):
    """
    Logs a debug-level message.
    
    Args:
        msg: The message to log.
    """
    pass
