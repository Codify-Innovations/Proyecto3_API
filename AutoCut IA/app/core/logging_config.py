import logging

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(levelname)s | %(asctime)s | %(name)s | %(message)s",
)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.INFO)