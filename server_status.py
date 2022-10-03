import requests


def is_site_running(site_url: str):
    try:
        response = requests.get(site_url)
        return response.ok
    except Exception as e:
        print(f"ERROR occurred: {e}")
        return False


def run():
    input_mess = "Please enter the name of the website: "
    continue_mess = "Would you like to test another site? (y / n): "
    while True:
        name = input(input_mess)
        if is_site_running(name):
            print(f"{name} is up and running.")
        else:
            print(f"{name} is currently down or having issues.")

        cont_input = input(continue_mess)
        if cont_input not in ['y', 'Y']:
            break


if __name__ == "__main__":
    run()
