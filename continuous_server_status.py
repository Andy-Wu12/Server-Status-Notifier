import requests
import smtplib
import email
import sys
import json
import datetime

from typing import TypedDict, List


Site_Status = TypedDict('Site_Status', {'url': str, 'status': bool})
Config_Data = TypedDict('Config_Data', {'email': str, 'urls': List[str]})


def is_site_running(site_url: str):
    """Ping desired site

    :arg
        site_url: A website url string.

    :returns
        A boolean value indicating whether the status code from a GET request
        to site_url is OK (< 400).
        In the case that the url is invalid or an exception is raised,
        the function returns False.
    """

    try:
        response = requests.get(site_url)
        return response.ok
    except Exception as e:
        print(f"ERROR occurred: {e}")
        return False


def send_status_email(user_email: str, statuses: Site_Status):
    """Send an email mentioning status of websites

        :arg
            user_email: Email address to send status messages to.
        :arg
            statuses: Dictionary of form {'url' : 'status'} indicating whether the website \
            is currently down or experiencing issues
        :returns
            Boolean indicating whether the email was successfully sent.
    """
    pass


def run(config_data: Config_Data):
    """Main function

        :arg
            config_file_path: A string representing the path to your JSON configuration file \
            where the list of websites to check and an (optional) email are stored.
    """
    user_email = config_data.get('email')
    urls = config_data.get('urls')

    next_check_interval = datetime.datetime.now()

    while True:
        if datetime.datetime.now() >= next_check_interval:
            for url in urls:
                print(f"Is {url} running?: {is_site_running(url)}")
            # Immediate return for testing
            next_check_interval += datetime.timedelta(minutes=30)
            return "Done"

def parseConfigData(filepath: str):
    with open(filepath) as f:
        data = json.load(f)

    return data


if __name__ == "__main__":
    # Read in command line argument for config file path
    try:
        config_path = sys.argv[1]
    except IndexError:
        sys.exit("A filepath must be provided for the location of your configuration file!")

    config_json = parseConfigData(config_path)
    run(config_json)
