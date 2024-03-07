# Site Monitor for Raspberry PI
Purpose: Monitor Site Availability from a Raspberry PI

## Raspberry PI Setup
1. Open a terminal and go to the folder to clone the project into.

2. Run the following commands.
```cmd
sudo apt-get install chromium-chromedriver
sudo apt-get install chromium-browser
sudo apt-get install xvfb xserver-xephyr vnc4server
git clone https://github.com/travis-mann/site_monitor
cd site_monitor
python -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt

```

3. Create a copy of config.json.dist and remove the ".dist" extension. Fill out the following values:
- "sender": Email address to send and receive monitoring notifications
- "site": Site URL
- "site_name": Informal website name for logging and notifications
- "username": Site username
- "password": Site password
- "username_id": element id for username input field
- "password_id": element id for password input field
- "expected_element_id": element id for an expected element post login
- "email_password": Email app password for smtp auth, https://support.google.com/mail/answer/185833?hl=en
- "max_check_attempts": Number of retries before reporting a failure
- "run_frequency_sec": Seconds between runs

4. Configure a cronjob to run main.py with the desired monitoring frequency.
