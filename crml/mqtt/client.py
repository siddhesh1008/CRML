import asyncio
import aiomqtt
from loguru import logger
from crml.config.settings import MqttSettings
from crml.mqtt.handlers import dispatch


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
                        await dispatch(str(message.topic), message.payload)
            except aiomqtt.MqttError as e:
                self._client = None
                logger.warning("MQTT disconnected: {}. Retrying in {}s", e, interval)
                await asyncio.sleep(interval)
                interval = min(interval * 2, 60)
