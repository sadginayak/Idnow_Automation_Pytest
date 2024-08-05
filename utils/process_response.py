from utils.logger_util import set_logger
from utils import api_requests as api_req
from utils.test_data_loader import TestDataLoader


class ResponseProcessor:
    def __init__(self, req_obj, test_data_file):
        self.logger = set_logger(__name__)
        self.req_obj = req_obj
        self.test_data_loader = TestDataLoader(test_data_file)
        self.test_data = self.test_data_loader.load_test_data()

    def get_response_and_statuscode(self, endpoint=""):
        """
        Forms the URL and executes the API request.

        :param endpoint: API endpoint
        :return: status_code, response
        """
        url = f"{self.req_obj.base_url}/{endpoint}"
        self.logger.info("Accessing URL: %s", url)
        try:
            status_code, response = self.req_obj.execute_api_request(request_type=api_req.GET_METHOD, endpoint=endpoint)
            self.logger.info("Response code: %s", status_code)
            return status_code, response
        except Exception as e:
            self.logger.error("Error executing API request to %s: %s", url, str(e))
            raise

    def process_response(self, response, key_path):
        try:
            value = response
            for key in key_path:
                value = value.get(key, {})
            if not value:
                raise KeyError(f"The key path {'.'.join(key_path)} is not found in the response")
            self.logger.info("Processed response for key path: %s", ".".join(key_path))
            return value
        except KeyError as e:
            self.logger.error("KeyError: %s", str(e))
            raise
        except Exception as e:
            self.logger.error("Error processing response: %s", str(e))
            raise

    def validate_support_matrix(self, support_matrix_response, minimum_supported_versions, matrix_type):
        validation_errors = []

        try:
            support_matrix = support_matrix_response.get('browserSupportMatrix', {}).get(matrix_type, {})
            if not support_matrix:
                validation_errors.append(
                    f"Support matrix does not contain '{matrix_type}' under 'browserSupportMatrix'")
                return validation_errors

            for platform, browsers in support_matrix.items():
                for browser, browser_info in browsers.items():
                    if browser in minimum_supported_versions:
                        browser_version = browser_info.get('min')
                        self.logger.info("On platform: %s Found browser: %s with version: %s", platform, browser,
                                         browser_version)
                        if browser_version is None:
                            validation_errors.append(f"'{browser}' does not contain 'min' version: {browser_info}")
                        elif browser_version < minimum_supported_versions[browser]:
                            validation_errors.append(
                                f"{browser} version {browser_version} on {platform} is less than {minimum_supported_versions[browser]}")

            self.logger.info("Validation completed with %d error(s)", len(validation_errors))
            return validation_errors

        except Exception as e:
            self.logger.error("Error validating support matrix: %s", str(e))
            raise
