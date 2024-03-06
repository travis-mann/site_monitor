# Site Monitor for Raspberry PI
Purpose: Monitor Site Availability from a Raspberry PI

## Raspberry PI Setup
1. Open a terminal and go to the folder to clone the project to

2. Run the following commands
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

3. Set the following environment variables:
- SENDER: Email address to send and receive monitoring notifications
- SITE: Site URL
- SITE_NAME: Informal website name for logging and notifications
- USERNAME_ID: element id for username input field
- PASSWORD_ID: element id for password input field
- PASSWORD: Site password
- USERNAME: Site username
- EMAIL_PASSWORD: Email app password for smtp auth, https://support.google.com/mail/answer/185833?hl=en

4. Configure a cronjob to run main.py with the desired monitoring frequency
