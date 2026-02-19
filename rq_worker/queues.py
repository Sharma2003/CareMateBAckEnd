from rq import Queue
from dotenv import load_dotenv
load_dotenv()
from redis import Redis

redis_conn=Redis(
    host="localhost",
    port=6380,
    db=0,
    decode_responses=False
)

report_queue = Queue(
    name="report-generation",
    connection=redis_conn,
    default_timeout=200    #10 mins
)
