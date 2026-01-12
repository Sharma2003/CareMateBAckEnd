import os
from langgraph.checkpoint.redis.aio import AsyncRedisSaver
from chat.src.graph.graph_redis import build_app

graph_app = None

async def init_graph():
    global graph_app
    async with AsyncRedisSaver.from_conn_string(os.getenv("REDIS_DB")) as saver:
        await saver.asetup()

        graph_app = build_app(checkpointer=saver)