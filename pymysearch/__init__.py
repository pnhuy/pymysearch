import os
import logging

logging.basicConfig(
    format='%(levelname)s:%(name)s:%(filename)s:%(message)s',
    level=os.getenv('LOG_LEVEL', logging.INFO)
)
logger = logging.getLogger(__name__)
