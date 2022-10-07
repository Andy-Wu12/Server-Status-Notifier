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

# Type annotations
Status_Data = List[TypedDict('Status_Data', {'url': str, 'status': str})]
Config_Data = TypedDict('Config_Data', {'recipients': List[str], 'urls': List[str],
                                        'emails_fail_only': bool, 'check_interval_secs': int})


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
        server.sendmail(user_email, recipients, msg.as_string())
        server.quit()
        print('email success!')
    return True


def run(config_data: Config_Data):
    """Main function

        :arg
            config_file_path: A string representing the path to your JSON configuration file \
            where the list of websites to check, an email, and a time interval (in secs) are stored.
    """
    recipients = config_data.get('recipients')
    urls = config_data.get('urls')
    downtime = config_data.get('check_interval_secs')
    emails_on_fail_only = config_data.get('emails_fail_only')

    if None in [recipients, urls, downtime, emails_on_fail_only]:
        print('A key is missing from your configuration!')
        print('Please make sure you have all keys as shown in the configuration template.')
        return None

    while True:
        url_statuses = []
        for url in urls:
            running = is_site_running(url)
            url_data = {'url': url,
                        'status': 'Online' if running else 'Offline'}
            if (emails_on_fail_only and not running) or not emails_on_fail_only:
                url_statuses.append(url_data)

        # Send email regarding status checks
        send_status_email(recipients, url_statuses)

        time.sleep(downtime)


def parseConfigData(filepath: str):
    try:
        with open(filepath) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise e

    return data


if __name__ == "__main__":
    user_email = os.getenv('USER_EMAIL')
    # Most likely necessary if using gmail or any other highly secure mailing client
    app_password = os.getenv('APP_PASSWORD')

    # Read in command line argument for config file path
    try:
        config_path = sys.argv[1]
    except IndexError:
        sys.exit("A filepath must be provided for the location of your configuration file!")

    try:
        config_json = parseConfigData(config_path)
        run(config_json)
    except json.JSONDecodeError:
        print("Error in parsing JSON. Please check your file for syntax errors!")
    except FileNotFoundError:
        print("The filename you entered does not exist!")
