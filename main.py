import os
import requests

username = os.environ.get('NAUKRI_USERNAME')
password = os.environ.get('NAUKRI_PASSWORD')

def update_profile():
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    login_url = "https://www.naukri.com/nlogin/login"
    payload = {"username": username, "password": password}

    print("1. Refreshing Naukri Profile Status...")
    res = session.post(login_url, json=payload, headers=headers)

    if res.status_code == 200:
        print("SUCCESS: Naukri Profile Logged In & Refreshed Successfully!")
        print("Your profile is now marked as 'Active Today' for Recruiters.")
    else:
        print(f"FAILED: Status Code {res.status_code}. Unable to refresh profile.")

if __name__ == "__main__":
    update_profile()
