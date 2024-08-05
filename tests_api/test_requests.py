import pytest
from configuration.configuration import BASE_URL
from utils import api_requests as api_req
from utils.logger_util import set_logger
from utils.process_response import ResponseProcessor

# Path to the YAML file
TEST_DATA_FILE = "test_data/api_testdata.yml"


@pytest.fixture(scope="class")
def class_fixture(request):
    """
    Class fixture to initialize APIRequests instance. This fixture will execute once before class execution.
    """
    request.cls.req_obj = api_req.APIRequests(base_url=BASE_URL)
    request.cls.logger = set_logger(__name__)
    request.cls.response_processor = ResponseProcessor(request.cls.req_obj, TEST_DATA_FILE)
    return


@pytest.mark.usefixtures("class_fixture")
class TestRequestsMethods(object):

    def test_execute_get_method(self):
        """
        Method to execute GET request and verify returned status code and response.
        """
        try:
            self.logger.info("Execute GET request test")
            # Use the get_response method to get the status code and response
            status_code, response = self.response_processor.get_response_and_statuscode(endpoint="")

            # Assert the status code is 200
            assert status_code == 200, "Expected status code is : {} but received status code : {}".format(200,
                                                                                                           status_code)

            # fetch test data from yml
            autoident_web_minimum_supported_versions = self.response_processor.test_data[
                "autoident_web_minimum_supported_versions"]
            autoident_web_key_path = self.response_processor.test_data["autoident_web_key_path"]

            # Extract the 'autoident_key' section
            autoident_web_key_response = self.response_processor.process_response(response, autoident_web_key_path)
            assert autoident_web_key_response is not None, "'autoident_key' does not contain 'web_key'"

            # minimum version supported in each of the platforms
            validation_errors = self.response_processor.validate_support_matrix(autoident_web_key_response,
                                                                                autoident_web_minimum_supported_versions,
                                                                                'desktop')

            # Handle validation errors
            assert not validation_errors, "Validation errors found: {}".format(validation_errors)
        except Exception as e:
            self.logger.error("Error: %s", str(e))
            raise

