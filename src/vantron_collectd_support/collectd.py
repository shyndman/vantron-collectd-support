from collections.abc import Generator
from functools import partial

from ha_mqtt_discoverable.sensors import BinarySensorInfo, DeviceInfo, EntityInfo, SensorInfo
from stringcase import capitalcase, spinalcase

from vantron_collectd_support.util import _nn_

DISK_FREE_ROOT_FS = "root"
type StateTopicPath = str


def _populate(entity: EntityInfo):
    entity.object_id = spinalcase(entity.name.lower())
    entity.unique_id = spinalcase(f"{_nn_(entity.device).name} {entity.name}".lower())
    if entity.expire_after is not None:
        entity.expire_after = 120  # seconds

    return entity


def _value_template_for_index(i: int, cast_expr: str = " | float(0.0)", transform_expr: str = "") -> str:
    return f"{{{{ value.split(':')[{i}].split('\0')[0] {cast_expr} {transform_expr} }}}}"


def uptime_topics(device: DeviceInfo) -> Generator[tuple[EntityInfo, StateTopicPath]]:
    yield (
        _populate(
            SensorInfo(
                name="Up Since",
                device=device,
                device_class="timestamp",
                value_template="{%- set now_ts = now() %}\n"
                + "{%- set now_ts = now_ts.replace(microsecond=0, second=0) %}\n"
                + "{{ (value.split(':')[1].split('\0')[0]|int // 60 * 60) | string | as_timedelta  * -1 + now_ts }}",
                unique_id="",
            )
        ),
        "uptime/uptime",
    )


def cpu_topics(device: DeviceInfo) -> Generator[tuple[EntityInfo, StateTopicPath]]:
    shared_args = {
        "device": device,
        "unit_of_measurement": "%",
        "suggested_display_precision": 1,
        "unique_id": "",
        "value_template": _value_template_for_index(1),
        "icon": "mdi:chip",
    }

    yield (
        _populate(SensorInfo(name="CPU Percent User", **shared_args)),
        "cpu/percent-user",
    )
    yield (
        _populate(SensorInfo(name="CPU Percent Interrupt", **shared_args)),
        "cpu/percent-interrupt",
    )
    yield (
        _populate(SensorInfo(name="CPU Percent Soft IRQ", **shared_args)),
        "cpu/percent-softirq",
    )
    yield (
        _populate(SensorInfo(name="CPU Percent Steal", **shared_args)),
        "cpu/percent-steal",
    )
    yield (
        _populate(SensorInfo(name="CPU Percent Idle", **shared_args)),
        "cpu/percent-idle",
    )
    yield (
        _populate(SensorInfo(name="CPU Percent Wait", **shared_args)),
        "cpu/percent-wait",
    )
    yield (
        _populate(SensorInfo(name="CPU Percent System", **shared_args)),
        "cpu/percent-system",
    )
    yield (
        _populate(
            SensorInfo(
                name="CPU Temperature",
                device=device,
                device_class="temperature",
                unit_of_measurement="°C",
                suggested_display_precision=1,
                unique_id="",
                value_template=_value_template_for_index(1),
            )
        ),
        "thermal-thermal_zone0/temperature",
    )


def load_topics(device: DeviceInfo) -> Generator[tuple[EntityInfo, StateTopicPath]]:
    shared_args = {
        "device": device,
        "device_class": "data_size",
        "unit_of_measurement": "%",
        "suggested_display_precision": 1,
        "unique_id": "",
    }

    load_value_template = partial(_value_template_for_index, transform_expr=" * 100.0")
    yield (
        _populate(SensorInfo(name="Load Avg. 1min", value_template=load_value_template(1), **shared_args)),
        "load/load",
    )
    yield (
        _populate(SensorInfo(name="Load Avg. 5min", value_template=load_value_template(2), **shared_args)),
        "load/load",
    )
    yield (
        _populate(SensorInfo(name="Load Avg. 15min", value_template=load_value_template(3), **shared_args)),
        "load/load",
    )


def memory_topics(device: DeviceInfo) -> Generator[tuple[EntityInfo, StateTopicPath]]:
    shared_args = {
        "device": device,
        "device_class": "data_size",
        "unit_of_measurement": "%",
        "suggested_display_precision": 1,
        "unique_id": "",
        "value_template": _value_template_for_index(1),
        "icon": "mdi:memory",
    }

    yield (
        _populate(SensorInfo(name="Memory Percent Free", **shared_args)),
        "memory/percent-free",
    )
    yield (
        _populate(SensorInfo(name="Memory Percent Buffered", **shared_args)),
        "memory/percent-buffered",
    )
    yield (
        _populate(SensorInfo(name="Memory Percent Cached", **shared_args)),
        "memory/percent-cached",
    )
    yield (
        _populate(SensorInfo(name="Memory Percent Used", **shared_args)),
        "memory/percent-used",
    )


def disk_free_topics(
    device: DeviceInfo,
    fs_name: str,
) -> Generator[tuple[EntityInfo, StateTopicPath]]:
    shared_args = {
        "device": device,
        "device_class": "data_size",
        "unit_of_measurement": "B",
        "suggested_display_precision": 0,
        "unique_id": "",
        "value_template": _value_template_for_index(1),
    }

    fs_label = capitalcase(fs_name)
    yield (
        _populate(SensorInfo(name=f"{fs_label} Bytes Free", **shared_args)),
        f"df-{fs_name}/df_complex-free",
    )
    yield (
        _populate(SensorInfo(name=f"{fs_label} Bytes Reserved", **shared_args)),
        f"df-{fs_name}/df_complex-reserved",
    )
    yield (
        _populate(SensorInfo(name=f"{fs_label} Bytes Used", **shared_args)),
        f"df-{fs_name}/df_complex-used",
    )


def network_topics(device: DeviceInfo, ping_host="1.1.1.1") -> Generator[tuple[EntityInfo, StateTopicPath]]:
    yield (
        _populate(
            BinarySensorInfo(
                name="Network Online",
                device=device,
                device_class="connectivity",
                unique_id="",
                payload_on="ON",
                payload_off="OFF",
            )
        ),
        "pppoe-wwan",
    )
    yield (
        _populate(
            SensorInfo(
                name=f"{ping_host} Avg. Ping Time",
                device=device,
                device_class="duration",
                unit_of_measurement="ms",
                suggested_display_precision=1,
                unique_id="",
                value_template=_value_template_for_index(1),
            )
        ),
        f"ping/ping-{ping_host}",
    )
    yield (
        _populate(
            SensorInfo(
                name="DHCP Leases",
                device=device,
                icon="mdi:ip",
                state_class="measurement",
                suggested_display_precision=0,
                unique_id="",
                value_template=_value_template_for_index(1),
            )
        ),
        "dhcpleases/count",
    )
    yield (
        _populate(
            SensorInfo(
                name="Wired Outgoing Traffic Rate",
                device=device,
                device_class="data_rate",
                unit_of_measurement="B/s",
                suggested_display_precision=1,
                icon="mdi:router-network",
                unique_id="",
                value_template=_value_template_for_index(1),
            )
        ),
        "interface-br-lan/if_octets",
    )
    yield (
        _populate(
            SensorInfo(
                name="Wired Incoming Traffic Rate",
                device=device,
                device_class="data_rate",
                unit_of_measurement="B/s",
                suggested_display_precision=1,
                icon="mdi:router-network",
                unique_id="",
                value_template=_value_template_for_index(2),
            )
        ),
        "interface-br-lan/if_octets",
    )
    yield (
        _populate(
            SensorInfo(
                name="Wireless Outgoing Traffic Rate",
                device=device,
                device_class="data_rate",
                unit_of_measurement="B/s",
                suggested_display_precision=1,
                icon="mdi:router-network-wireless",
                unique_id="",
                value_template=_value_template_for_index(1),
            )
        ),
        "interface-rax0/if_octets",
    )
    yield (
        _populate(
            SensorInfo(
                name="Wireless Incoming Traffic Rate",
                device=device,
                device_class="data_rate",
                unit_of_measurement="B/s",
                suggested_display_precision=1,
                icon="mdi:router-network-wireless",
                unique_id="",
                value_template=_value_template_for_index(2),
            )
        ),
        "interface-rax0/if_octets",
    )
