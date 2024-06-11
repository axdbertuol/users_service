import asyncio
from contextlib import asynccontextmanager

from aiokafka import AIOKafkaProducer
from fastapi import FastAPI

from .config import get_settings

loop = asyncio.get_event_loop()
aioproducer = None


def get_aioproducer():
    global aioproducer
    return aioproducer


@asynccontextmanager
async def lifespan(app: FastAPI):
    global aioproducer
    aioproducer = AIOKafkaProducer(
        loop=loop, bootstrap_servers=get_settings().kafka_url
    )
    await aioproducer.start()
    yield
    await aioproducer.stop()
