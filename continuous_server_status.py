import requests
import smtplib
import email
import sys

from typing import TypedDict


Site_Status = TypedDict('Site_Status', {'url': str, 'status': bool})


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
    pass


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


def run(config_file_path: str):
    """Main function

        :arg
            config_file_path: A string representing the path to your JSON configuration file \
            where the list of websites to check and your (optional) email are stored.
    """
    pass


if __name__ == "__main__":
    # Read in command line argument for config file path
    try:
        config_path = sys.argv[1]
    except IndexError:
        sys.exit("A filepath must be provided for the location of your configuration file!")

    run(config_path)
