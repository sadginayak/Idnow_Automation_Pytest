from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger_util import set_logger


class QuitSessionPage:

    def __init__(self, driver, platform_data):
        self.driver = driver
        self.platform_data = platform_data
        self.logger = set_logger(__name__)

    def validate_screen_displayed_and_choose_option_and_quit(self):
        try:
            options_display = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.XPATH, self.platform_data['quit_identification_display_xpath']))
            )
            if options_display.is_displayed():
                self.logger.info("Option and quit screen is displayed")
                quit_reason_radio_button = self.driver.find_element(AppiumBy.XPATH,
                                                                    self.platform_data['options_radio_button_xpath'])
                quit_reason_radio_button.click()

                quit_button = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((AppiumBy.XPATH, self.platform_data['quit_button_xpath']))
                )
                if quit_button.is_enabled():
                    quit_button.click()
                else:
                    raise Exception("Quit session button is not enabled")
            else:
                raise Exception("Option and quit screen was not found")
        except Exception as e:
            raise Exception(f"Error choosing option and quitting: {str(e)}")
