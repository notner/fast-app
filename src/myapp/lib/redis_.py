import asyncio
import redis.asyncio as redis


class Redis:
    def __init__(
        self,
        host: str,
        port: int,
        db: str
    ):
        self._host = host
        self._port = port
        self._db = db

        self._pool = redis.ConnectionPool(
            host=self._host,
            port=self._port,
            db=self._db
        )
        self._client = None

    async def client(self):
        if not self._client:
            self._client = await redis.Redis(connection_pool=self._pool)
        return self._client

    async def set(self, key: str, value: str, expire=None) -> bool:
        return await self.client().set(key, value)

    async def get(self, key):
        return await self.client().get(key)


# Async Reader for Channel
async def reader(channel: redis.client.PubSub, callback):
    while True:
        try:
            async with asyncio.timeout(10):
                message = await channel.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    await callback()
                await asyncio.sleep(5)  # wait to check again
        except (asyncio.TimeoutError):
            # We only get here if something takes longer
            # than the timeout in the loop
            pass
