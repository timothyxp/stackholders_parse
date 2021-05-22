import os
from src.utils.logger import logger


class Config:
    def __init__(self):
        self.project_path = os.path.dirname(__file__)
        logger.debug(f"start from {self.project_path}")

        self.data_path = os.path.join(self.project_path, "data")
        os.makedirs(self.data_path, exist_ok=True)

        self.cache_path = os.path.join(self.data_path, "cache_path")
        os.makedirs(self.cache_path, exist_ok=True)

        self.pages_cache_dir = os.path.join(self.cache_path, "pages_cache")
        os.makedirs(self.pages_cache_dir, exist_ok=True)

        self.parsed_data_file = os.path.join(self.data_path, "parsed_texts.parquet")


config = Config()
