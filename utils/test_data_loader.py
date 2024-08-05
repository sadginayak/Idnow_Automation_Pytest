import yaml
import logging


class TestDataLoader:
    def __init__(self, test_data_file):
        self.test_data_file = test_data_file
        self.logger = logging.getLogger(__name__)

    def load_test_data(self):
        try:
            with open(self.test_data_file, 'r') as file:
                data = yaml.safe_load(file)
            self.logger.info("Test data loaded successfully from %s", self.test_data_file)
            return data
        except Exception as e:
            self.logger.error("Error loading test data from %s: %s", self.test_data_file, str(e))
            raise

    def get_platform_data(self, platform):
        data = self.load_test_data()
        platform_data = data.get('Platform', {}).get(platform.lower())
        if not platform_data:
            raise ValueError(f"No data found for platform: {platform}")
        self.logger.info(f"Test data for platform {platform} loaded successfully")
        return platform_data