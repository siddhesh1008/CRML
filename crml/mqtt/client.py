import asyncio
import aiomqtt
from loguru import logger
from crml.config.settings import MqttSettings
from crml.mqtt.handlers import dispatch
from crml.ha.discovery import discovery_payloads, available_topic

_KNOWN_ROBOTS: set[str] = set()


class MQTTBridge:
    def __init__(self, settings: MqttSettings):
        self._settings = settings
        self._client: aiomqtt.Client | None = None

    @property
    def is_connected(self) -> bool:
        return self._client is not None

    async def publish(self, topic: str, payload: str) -> None:
        if self._client:
            await self._client.publish(topic, payload)

    async def announce_robot(self, robot_id: str) -> None:
        if robot_id in _KNOWN_ROBOTS:
            return
        _KNOWN_ROBOTS.add(robot_id)
        for topic, payload in discovery_payloads(robot_id):
            await self.publish(topic, payload)
        await self.publish(available_topic(robot_id), "online")
        logger.info("Announced robot '{}' to Home Assistant", robot_id)

    async def run(self) -> None:
        interval = 5
        while True:
            try:
                async with aiomqtt.Client(
                    hostname=self._settings.host,
                    port=self._settings.port,
                    identifier=self._settings.client_id,
                ) as client:
                    self._client = client
                    await client.subscribe(self._settings.topics.subscribe)
                    logger.info("MQTT connected to {}:{}, subscribed to '{}'",
                                self._settings.host, self._settings.port,
                                self._settings.topics.subscribe)
                    interval = 5
                    async for message in client.messages:
                        topic = str(message.topic)
                        parts = topic.split("/")
                        if parts[0] == "robots" and len(parts) >= 3:
                            await self.announce_robot(parts[1])
                        await dispatch(topic, message.payload)
            except aiomqtt.MqttError as e:
                self._client = None
                logger.warning("MQTT disconnected: {}. Retrying in {}s", e, interval)
                await asyncio.sleep(interval)
                interval = min(interval * 2, 60)
