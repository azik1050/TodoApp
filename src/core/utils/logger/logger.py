import sys

from loguru import logger

from core.utils.data_generator.data_generator import DataGenerator


class Logger:
    def __init__(self):
        self.logger = logger
        logger.remove()
        logger.add(
            sys.stdout,
            format=("{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"),
            level="INFO",
        )

    def info(self, message: str):
        self.logger.info(f"[{DataGenerator.get_guid()}] {message}")

    def error(self, message: str):
        self.logger.error(f"[{DataGenerator.get_guid()}] {message}")

console_logger = Logger()