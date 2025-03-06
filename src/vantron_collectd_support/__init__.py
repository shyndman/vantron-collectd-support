import functools
import itertools
from collections.abc import Generator

from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import BinarySensor, BinarySensorInfo, DeviceInfo, EntityInfo, Sensor, SensorInfo
from loguru import logger
from stringcase import spinalcase

from vantron_collectd_support.collectd import (
    DISK_FREE_ROOT_FS,
    StateTopicPath,
    cpu_topics,
    disk_free_topics,
    load_topics,
    memory_topics,
    network_topics,
    uptime_topics,
)
from vantron_collectd_support.const import CLIENT_ID, STATE_PREFIX
from vantron_collectd_support.util import _nn_


def pi_sensors() -> Generator[tuple[EntityInfo, StateTopicPath]]:
    device = DeviceInfo(
        name="Vantron",
        identifiers=["7135376c756a5f2a"],
        model="Raspberry Pi 5",
        manufacturer="Raspberry Pi Foundation",
        connections=[("eth0 mac", "2c:cf:67:6d:e7:58")],
    )

    yield from uptime_topics(device)
    yield from cpu_topics(device)
    yield from load_topics(device)
    yield from memory_topics(device)
    yield from disk_free_topics(device, DISK_FREE_ROOT_FS)


def router_sensors() -> Generator[tuple[EntityInfo, StateTopicPath]]:
    device = DeviceInfo(
        name="Vnet",
        identifiers=["yx87fec"],
        model="Beryl AX (GL-MT3000)",
        manufacturer="GL.iNet",
        connections=[("eth0 mac", "94:83:c4:58:7f:ec")],
    )

    yield from uptime_topics(device)
    yield from cpu_topics(device)
    yield from load_topics(device)
    yield from memory_topics(device)
    yield from disk_free_topics(device, DISK_FREE_ROOT_FS)
    yield from network_topics(device)


def add_discovery_topics():
    logger.info("Adding CollectD Discovery Topics")

    mqtt = Settings.MQTT(host="0.0.0.0", client_name=CLIENT_ID, state_prefix=STATE_PREFIX)

    for entity, entity_topic in itertools.chain(pi_sensors(), router_sensors()):
        d = build_discoverable(entity, mqtt, get_topic_gen(_nn_(entity.device), entity_topic))
        s = d.write_config()
        if s is not None:
            s.wait_for_publish()


def get_topic_gen(device: DeviceInfo, entity_topic: str):
    topic = f"collectd/{spinalcase(device.name)}/{entity_topic}"
    return functools.partial(lambda _, topic: topic, topic=topic)


def build_discoverable(entity: EntityInfo, mqtt: Settings.MQTT, topic_gen):
    match entity:
        case SensorInfo():
            return Sensor(Settings(mqtt=mqtt, entity=entity), make_state_topic=topic_gen)

        case BinarySensorInfo():
            return BinarySensor(Settings(mqtt=mqtt, entity=entity), make_state_topic=topic_gen)

        case _:
            raise ValueError(f"{entity} must represent sensor or binary_sensor")
