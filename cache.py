import redis.asyncio as redis
import os

r = redis.from_url(os.getenv("REDIS_URL"))

async def set_cache(k,v):
    await r.set(k,v,ex=300)

async def get_cache(k):
    return await r.get(k)
