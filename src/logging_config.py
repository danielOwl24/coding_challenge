import logging
from logging.handlers import RotatingFileHandler
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

log_file = "logs/app.log"
log_level = logging.INFO

logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(log_file, maxBytes=1000000, backupCount=3, mode="w"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)