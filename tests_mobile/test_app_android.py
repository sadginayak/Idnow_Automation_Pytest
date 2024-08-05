import time

import pytest

from pages.autoIdent_home_page import AutoIdentHomePage
from pages.intermediate_screen_page import IntermediateScreenPage
from pages.quit_session_page import QuitSessionPage
from pages.terms_and_conditions_page import TermsAndConditionsPage
from utils.logger_util import set_logger
from utils.mobile_util import MobileAutomation
from utils.test_data_loader import TestDataLoader

# Path to the YAML file
BS_TEST_DATA_FILE = "test_data/browserstack.yml"
INPUT_TEST_DATA_FILE = "test_data/mobile_testdata.yml"


@pytest.fixture(scope="class")
def setup_class(request):
    """
    Class fixture to initialize MobileAutomation instance.
    """
    request.cls.logger = set_logger(__name__)
    request.cls.platform = 'android'
    request.cls.mobile_automation = MobileAutomation(BS_TEST_DATA_FILE)
    request.cls.driver = request.cls.mobile_automation.start_mobile_session(request.cls.platform)

    # Load platform-specific test data
    test_data_loader = TestDataLoader(INPUT_TEST_DATA_FILE)
    platform_data = test_data_loader.get_platform_data(request.cls.platform)

    # Initialize page objects
    request.cls.autoident_home_page = AutoIdentHomePage(request.cls.driver, platform_data)
    request.cls.terms_and_conditions_page = TermsAndConditionsPage(request.cls.driver, platform_data)
    request.cls.quit_session_screen_page = QuitSessionPage(request.cls.driver, platform_data)
    request.cls.intermediate_screen_page = IntermediateScreenPage(request.cls.driver, platform_data)


@pytest.mark.usefixtures("setup_class")
class TestAndroidMobileApp(object):

    def test_mobile_app(self):

        self.logger.info("Execute mobile app test")
        try:

            # Launch the application
            self.autoident_home_page.launch_application()
            # Validate home screen elements
            ident_box, start_button = self.autoident_home_page.validate_home_screen_elements()
            assert ident_box is not None, "Ident ID text box not found on home screen"
            assert start_button is not None, "Start Ident button not found on home screen"

            self.autoident_home_page.enter_ident_id_and_start()

            # Validate terms and conditions screen
            terms_conditions_display, close_icon = self.terms_and_conditions_page.validate_terms_conditions_screen_elements()
            assert terms_conditions_display is not None, "Terms and Conditions screen not displayed"
            assert close_icon is not None, "Close icon not found"

            # Choose an option and quit
            self.quit_session_screen_page.validate_screen_displayed_and_choose_option_and_quit()

            # Validate intermediate screen
            intermediate_screen_element = self.intermediate_screen_page.validate_intermediate_screen()
            assert intermediate_screen_element is not None, "Intermediate screen not displayed"

            time.sleep(2)  # Adjust time if needed

            self.logger.info("Mobile app test completed successfully.")

            self.mobile_automation.end_mobile_session(self.driver)

        except Exception as e:
            self.mobile_automation.end_mobile_session(self.driver)
            self.logger.error(f"Error in mobile app test: {str(e)}")
            raise
