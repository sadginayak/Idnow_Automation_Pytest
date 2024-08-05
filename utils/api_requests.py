"""
This file contains common methods to execute API requests.
"""

import requests
from utils.logger_util import set_logger


# Global defines
GET_METHOD = "GET"
POST_METHOD = "POST"
PUT_METHOD = "PUT"
DELETE_METHOD = "DELETE"


class APIRequests:

    def __init__(self, base_url, req_timeout=10):
        """
        Initializing APIRequests.
        :param base_url: Base URL.
        :param req_timeout: request timeout.
        """
        self.base_url = base_url
        self.headers = {
            'Accept': 'application/json',
        }
        self.timeout = req_timeout
        self.logger = set_logger(__name__)

    def execute_api_request(self, request_type, endpoint, data="", header=""):
        """
        Method to execute given requests (GET, POST, PUT, DELETE).
        :param request_type: request type that want to execute
        :param endpoint: API endpoint
        :param data: API data
        :param header: API header
        :return: status_code: API status code
                response: API returned response
        """
        self.logger.info(f"Execute API request for URL:{self.base_url}/{endpoint}")
        response, status_code = "", None
        if header == "":
            header = self.headers
        try:
            baseurl = self.base_url if not endpoint else f"{self.base_url}/{endpoint}"
            if request_type == GET_METHOD:
                response = requests.get(url=baseurl, headers=header, timeout=self.timeout)
            elif request_type == POST_METHOD:
                response = requests.post(url=baseurl, headers=header, data=data, timeout=self.timeout)
            elif request_type == PUT_METHOD:
                response = requests.put(url=baseurl, headers=header, data=data, timeout=self.timeout)
            elif request_type == DELETE_METHOD:
                response = requests.delete(url=baseurl, timeout=self.timeout)
            else:
                response = "Invalid request type found"
            status_code = response.status_code
            response = response.json()
        except requests.exceptions.HTTPError as exhttp:
            response = exhttp
        except requests.exceptions.ConnectionError as exconn:
            response = exconn
        except requests.exceptions.Timeout as extimeout:
            response = extimeout
        except requests.exceptions.RequestException as exreq:
            response = exreq
        except Exception as ex:
            response = "Exception raised during execution of {} request, exception is : {}".format(request_type, ex)
        return status_code, response

