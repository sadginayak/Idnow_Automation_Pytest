from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger_util import set_logger


class AutoIdentHomePage:

    def __init__(self, driver, platform_data):
        self.driver = driver
        self.platform_data = platform_data
        self.logger = set_logger(__name__)

    def launch_application(self):
        # Start the mobile session
        if not self.driver:
            raise Exception("Driver not initialized.")
        self.logger.info("application launched successfully")

    def validate_home_screen_elements(self):
        try:
            ident_home_screen = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.CLASS_NAME, self.platform_data['idnow_logo_classname']))
            )
            if ident_home_screen.is_displayed():
                self.logger.info("Home screen displayed")
                ident_box = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((AppiumBy.CLASS_NAME, self.platform_data['ident_box_classname']))
                )
                start_button = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((AppiumBy.XPATH, self.platform_data['start_button_xpath']))
                )
                return ident_box, start_button
            else:
                raise Exception("Home screen element not found")
        except Exception as e:
            raise Exception(f"Error validating home screen elements: {str(e)}")

    def enter_ident_id_and_start(self):
        try:
            self.logger.info("Enter ident ID")
            ident_box = self.driver.find_element(AppiumBy.CLASS_NAME, self.platform_data['ident_box_classname'])
            ident_box.send_keys(self.platform_data['ident_id'])
            start_button = self.driver.find_element(AppiumBy.XPATH, self.platform_data['start_button_xpath'])
            if start_button.is_enabled():
                start_button.click()
            else:
                raise Exception("Start button is not enabled")
        except Exception as e:
            raise Exception(f"Error entering Ident ID and clicking start: {str(e)}")
