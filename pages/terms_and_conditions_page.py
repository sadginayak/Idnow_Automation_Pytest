from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger_util import set_logger


class TermsAndConditionsPage:

    def __init__(self, driver, platform_data):
        self.driver = driver
        self.platform_data = platform_data
        self.logger = set_logger(__name__)

    def validate_terms_conditions_screen_elements(self):
        try:
            terms_conditions_screen = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((AppiumBy.XPATH, self.platform_data['terms_conditions_xpath']))
            )
            if terms_conditions_screen.is_displayed():
                self.logger.info("Terms and conditions screen displayed")
                close_icon = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID,
                                                      self.platform_data['close_icon_accessibility_id'])
                close_icon.click()
            else:
                raise Exception("Terms and conditions screen element not found")

            return terms_conditions_screen, close_icon
        except Exception as e:
            raise Exception(f"Error validating terms and conditions screen elements: {str(e)}")
