import argparse
import importlib
import pytest
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Run specific tests with optional parameters.")
    parser.add_argument('--test', type=str, required=True, help='Test class to run (e.g., TestAPI or TestMobile)')
    parser.add_argument('--platform', type=str, choices=['android', 'ios'],
                        help='Platform to test on (required for TestMobile)')
    parser.add_argument('--username', type=str, help='BrowserStack username (required for TestMobile)')
    parser.add_argument('--access_key', type=str, help='BrowserStack access key (required for TestMobile)')
    parser.add_argument('--app_url', type=str, help='BrowserStack app URL (required for TestMobile)')
    return parser.parse_args()


def main():
    args = parse_args()

    if args.test == 'TestMobile':
        if not all([args.platform, args.username, args.access_key, args.app_url]):
            print("Error: --platform, --username, --access_key, and --app_url are required for TestMobile.")
            sys.exit(1)

        module_name = 'test_app_ios'
        test_class_name = 'TestMobileApp'
        platform = args.platform
        username = args.username
        access_key = args.access_key
        app_url = args.app_url

    elif args.test == 'tests_api':
        module_name = 'test_requests'
        test_class_name = 'TestRequestsMethods'
    else:
        print("Error: Invalid test class specified.")
        sys.exit(1)

    # Import the module and get the test class
    module = importlib.import_module(module_name)
    test_class = getattr(module, test_class_name)

    # Run the tests
    pytest_args = ["-v"]
    if args.test == 'TestMobile':
        pytest_args.extend(
            ["--platform", platform, "--username", username, "--access_key", access_key, "--app_url", app_url])
    pytest_args.append(f"{module_name}::{test_class_name}")

    pytest.main(pytest_args)


if __name__ == "__main__":
    main()
