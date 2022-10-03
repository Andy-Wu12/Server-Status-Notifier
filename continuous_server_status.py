import requests
import smtplib
import sys
import json
import os
import time

from dotenv import load_dotenv
from typing import TypedDict, List
from email.message import EmailMessage

load_dotenv()

user_email = os.getenv('USER_EMAIL')
# Most likely necessary if using gmail or any other secure mailing client
app_password = os.getenv('APP_PASSWORD')

# Type annotations
Status_Data = List[TypedDict('Status_Data', {'url': str, 'status': str})]
Config_Data = TypedDict('Config_Data', {'recipients': List[str], 'urls': List[str]})


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


def send_status_email(recipients: List[str], urls: Status_Data):
    """Send an email mentioning status of websites

        :arg
            user_email: Email address to send status messages to.
        :arg
            statuses: Dictionary of form {'url' : 'status'} indicating whether the website \
            is currently down or experiencing issues
        :returns
            Boolean indicating whether the email was successfully sent.
    """

    if not recipients or not urls:
        return False

    msg_body = ''.join([f'{url_data["url"]} status: {url_data["status"]}\n' for url_data in urls])

    msg = EmailMessage()
    msg.set_content(msg_body)

    msg['Subject'] = 'Your website status update'
    msg['From'] = user_email
    msg['To'] = recipients

    print(msg)
    # Send the message throught SMTP server on localhost
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(user_email, app_password)
        server.sendmail(user_email, [user_email], msg.as_string())
        server.quit()
        print('email success!')
    return True


def run(config_data: Config_Data):
    """Main function

        :arg
            config_file_path: A string representing the path to your JSON configuration file \
            where the list of websites to check and an (optional) email are stored.
    """
    recipients = config_data.get('recipients')
    urls = config_data.get('urls')

    while True:
        url_statuses = []
        for url in urls:
            url_data = {'url': url,
                        'status': 'Online' if is_site_running(url) else 'Offline'}
            url_statuses.append(url_data)

        # Send email regarding failed checks if email is provided
        send_status_email(recipients, url_statuses)

        # TODO: Allow for configuring interval between checks
        time.sleep(300)


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
