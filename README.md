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


Running the test to validate mobile solution for android, 
1. Signin to Broswerstack and select App Automate section.
2. Upload the ipa and apk file kept in mobile_app folder of the framework.
3. After successful upload, fetch the username, accesskey and app url. 
4. These details need to be provided in Browserstack.yml file in the framework under test_data directory in order to run the solution. Please update app url at two occurances to satisfy the capabilties.
5. Run the test using command - pytest tests_mobile/test_app_ios.py (for ios testing) or pytest tests_mobile/test_app_android.py(for android testing)
6. You can see the current execution in session created on Browserstack and the run results in logs.
