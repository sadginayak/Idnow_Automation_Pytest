from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
import browserstack.local
from configuration.configuration import BROWSERSTACK_URL
from utils.logger_util import set_logger
from utils.test_data_loader import TestDataLoader


class MobileAutomation:

    def __init__(self, test_data_file):
        self.setup_driver = None
        self.logger = set_logger(__name__)
        self.test_data_loader = TestDataLoader(test_data_file)
        self.test_data = self.test_data_loader.load_test_data()
        self.bs_local = None

    def start_browserstack_local(self):
        self.bs_local = browserstack.local.Local()
        bs_local_args = {
            "key": self.test_data['browserstack']['access_key'],
            "forcelocal": "true"  # Optional, depending on your use case
        }
        self.bs_local.start(**bs_local_args)
        if self.bs_local.isRunning():
            self.logger.info("BrowserStack Local started successfully.")
        else:
            raise Exception("Failed to start BrowserStack Local.")

    def stop_browserstack_local(self):
        if self.bs_local and self.bs_local.isRunning():
            self.bs_local.stop()
            self.logger.info("BrowserStack Local stopped successfully.")

    def prepare_capabilities(self, platform):
        """
        Prepare and return the desired capabilities with BrowserStack options.
        """
        capabilities = self.test_data.get('desired_capabilities', {}).get(platform, {})
        if not capabilities:
            raise ValueError(f"No capabilities found for platform: {platform}")

        capabilities['bstack:options'] = {
            'userName': self.test_data['browserstack']['username'],
            'accessKey': self.test_data['browserstack']['access_key']
        }

        self.logger.info(f"Prepared capabilities: {capabilities}")
        return capabilities

    def initialize_platform_options(self, platform, capabilities):
        """
        Initialize and return Appium options based on the platform.
        """
        if platform == 'ios':
            options = XCUITestOptions().load_capabilities(capabilities)
        elif platform == 'android':
            options = UiAutomator2Options().load_capabilities(capabilities)
        else:
            raise ValueError(f"Unsupported platform: {platform}")

        self.logger.info(f"Initialized options for platform {platform}: {options}")
        return options

    def setup(self, options):
        # Set up BrowserStack capabilities and start the session
        self.setup_driver = webdriver.Remote(
            command_executor=BROWSERSTACK_URL,
            options=options
        )
        return self.setup_driver

    def start_mobile_session(self, platform):
        try:
            # Start BrowserStack Local
            self.start_browserstack_local()

            # Prepare capabilities
            capabilities = self.prepare_capabilities(platform)

            # Initialize options
            options = self.initialize_platform_options(platform, capabilities)

            # Start the mobile session
            driver = self.setup(options)

            self.logger.info("Mobile options returned successfully.")
            return driver
        except KeyError as ke:
            self.logger.error(f"Key error in capabilities configuration: {ke}")
            raise
        except Exception as e:
            self.logger.error(f"Error starting mobile session: {str(e)}")
            raise

    def end_mobile_session(self, driver):
        # Clean up code, if needed
        driver.quit()
