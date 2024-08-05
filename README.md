## <h1>Setup:<h1>
- Download and install Python (Ignore the step if you already have python installed)
- Clone this repo, navigate to Idnow_Automation_Pytest folder.
- Execute requirements.txt file to install all the dependent python libraries using following command and make it pass without any error: pip install -r requirements.txt
- Update you browserstack username, accesskey and app url in browserstack.yml to execute the mobile test

# Project Structure

This project follows a structured approach to organizing code for automated testing. Below is a brief description of the key folders and files:

## `tests_api/ and tests_mobile`
Contains all test files for different platforms.

## `pages/`
Holds the Page Object Model (POM) classes that represent pages and UI elements of the application, with methods to interact with and validate these elements.

## `utils/`
Includes utility functions and classes for logging, data loading, api and mobile automation. Supports various functionalities needed for test execution.

## `test_data/`
Stores test data files, including BrowserStack configuration, api and mobile-specific test data.

## `configuration/`
Stores URL to testing platform.

For detailed instructions on running tests, refer to the relevant sections of this file.

## <h2>Running the tests:<h2>
- Run below command to execute all the tests in their respective folder. This will generate log file (with name: log-<YYMMDD_HHMMSS>.log) at current location.
pytest tests_api/
- or
pytest tests_mobile/
- Run below command to execute and generate pytest html report: 
pytest -vs --capture sys tests_api\test_requests.py --html=report.html
pytest -vs --capture sys tests_mobile\test_app_android.py --html=report.html

