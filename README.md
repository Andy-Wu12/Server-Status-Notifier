
# Website Status Notifier

A Python script that helps check the online status of a list of user-provided websites.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

# Installation
1. Download Python (Project developed using [Python 3.9](https://www.python.org/downloads/release/python-390/))
2. Clone this repository

# Ways to use
## 1. Temporarily
1. Run `python server_status.py`
2. Enter the name of the website you want to check including the protocol (http[s]) and the top-level domain
   1. Ex: `https://google.com`

## 2. Permanently
1. Additionally install the dotenv module with `pip install python-dotenv`
2. Modify the `config_template.json` file replacing the provided placeholders with your own data in the same format.
   1. You can rename the file as you wish, just make sure to pass the correct name when calling the script.
3. Create a .env file with your gmail address and [APP PASSWORD](https://support.google.com/accounts/answer/185833?hl=en)
   1. If you want to use a different mailing client, you will have to modify `perm_server_status` with the 
   client's required configuration.
   2. This program searches for environment variables named:
      1. USER_EMAIL
      2. APP_PASSWORD
4. Run `python perm_server_status.py config_template.json` to start the program.
   1. To stop the execution of the program, you can use CTRL-C or close the terminal instance.
