# rq_worker/worker.py

import sys, os

# Add project root to Python path (CRITICAL FIX)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rq import Queue, SimpleWorker
from redis import Redis

redis_conn = Redis(
    host="localhost",
    port=6380,
    db=0,
    decode_responses=False
)

listen = ["report-generation"]

if __name__ == "__main__":
    
    queues = [Queue(name, connection=redis_conn) for name in listen]
    worker = SimpleWorker(queues, connection=redis_conn)
    worker.work()
