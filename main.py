import requests
import os

username = os.environ.get('NAUKRI_USERNAME')
password = os.environ.get('NAUKRI_PASSWORD')

# Naukri Login & Profile Update Logic
login_url = "https://www.naukri.com/nlogin/login"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

payload = {
    "username": username,
    "password": password
}

session = requests.Session()
response = session.post(login_url, json=payload, headers=headers)

if response.status_code == 200:
    print("Naukri Login Successful! Profile status refreshed.")
else:
    print("Login Failed. Status Code:", response.status_code)
