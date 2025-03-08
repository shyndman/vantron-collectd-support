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
        pass

class Callback[EventT](Protocol):
    def __call__(self, event: EventT, data: object | None) -> None:
        pass

class LogCallback[EventT](Protocol):
    def __call__(self, severity: int, message: str, data: object | None) -> None:
        pass

class FlushCallback[EventT](Protocol):
    def __call__(self, timeout: int, id: str | None, data: object | None) -> None:
        pass

class NoEventCallback(Protocol):
    def __call__(self, data: object | None) -> None:
        pass

type CallbackIdentifier = str

def unregister_log(identifier: CallbackIdentifier) -> None:
    pass

def register_log(callback: LogCallback, data: object | None = None, name: str | None = None) -> CallbackIdentifier:
    pass

def unregister_config(identifier: CallbackIdentifier) -> None:
    pass

def register_config(callback: Callback[Config], data: object = None, name: str | None = None) -> CallbackIdentifier:
    pass

def unregister_init(identifier: CallbackIdentifier) -> None:
    pass

def register_init(callback: NoEventCallback, data: object = None, name: str | None = None) -> CallbackIdentifier:
    pass

def unregister_read(identifier: CallbackIdentifier) -> None:
    pass

def register_read(
    callback: NoEventCallback, interval_s: float = 0, data: object = None, name: str | None = None
) -> CallbackIdentifier:
    pass

def unregister_write(identifier: CallbackIdentifier) -> None:
    pass

def register_write(callback: Callback[Values], data: object = None, name: str | None = None) -> CallbackIdentifier:
    pass

def unregister_notification(identifier: CallbackIdentifier) -> None:
    pass

def register_notification(
    callback: Callback[Notification], data: object = None, name: str | None = None
) -> CallbackIdentifier:
    pass

def unregister_flush(identifier: CallbackIdentifier) -> None:
    pass

def register_flush(callback: FlushCallback, data: object = None, name: str | None = None) -> CallbackIdentifier:
    pass

def unregister_shutdown(identifier: CallbackIdentifier) -> None:
    pass

def register_shutdown(callback: NoEventCallback, data: object = None, name: str | None = None) -> CallbackIdentifier:
    pass

def get_dataset(name: str) -> List[Tuple[str, str, float | None, float | None]]:
    pass

def flush(plugin: str, timeout: int | None = -1, identifier: str | None = None):
    pass

def error(msg: str):
    pass

def warning(msg: str):
    pass

def notice(msg: str):
    pass

def info(msg: str):
    pass

def debug(msg: str):
    pass
