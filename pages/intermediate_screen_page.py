from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger_util import set_logger


class IntermediateScreenPage:

    def __init__(self, driver, platform_data):
        self.driver = driver
        self.platform_data = platform_data
        self.logger = set_logger(__name__)

    def validate_intermediate_screen(self):
        try:
            intermediate_screen_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.CLASS_NAME, self.platform_data['failure_screen_accessibility_id']))
            )
            ident_home_screen = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.CLASS_NAME, self.platform_data['idnow_logo_classname']))
            )
            if ident_home_screen.is_displayed():
                self.logger.info("Home screen displayed again")
                return intermediate_screen_element
            else:
                raise Exception("Home screen element not found")
        except Exception as e:
            raise Exception(f"Error validating intermediate screen: {str(e)}")
