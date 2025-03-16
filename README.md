# Automation Project
The OTP Gépkocsinyeremény Scraper:

- Scrapes the OTP Gépkocsinyeremény website using Selenium
- Runs inside a Docker container
- Uses a Bash script to execute a Python script
- Reads series_numbers from a .txt file
- Logs results and sends an email notification via msmtp + Gmail App Password
- Is fully automated with PowerShell + Task Scheduler on Windows

``` otp_gepkocsinyeremeny/
 │── docker/               # Stores docker image and requirements.txt
 │   ├── Dockerfile
 │   ├── requirements.txt
 │── scripts               # Stores scripts for automation
 │   ├── gepkocsi_betet.py
 │   ├── run_nyeremenybetet_script_mail.sh
 │── automation            # Mail sending client & Task Scheduler Powershell code
 │   ├── nyeremenybetet-idozito.ps1
 │   ├── msmtprc
 │── README.md
 │── .gitignore
```
# Setup Instructions
# Clone the Repository
```
git clone https://github.com/antalbalint97/automation/tree/otp_deposit
cd otp_deposit
```
# Configure msmtp for Gmail
Create the msmtprc configuration file:
```
vim ~/.msmtprc
```
Add the following:
```
account default
host smtp.gmail.com
port 587
auth on
tls on
user your-email@gmail.com
password your-gmail-app-password
from your-email@gmail.com
logfile ~/.msmtp.log
```
Then, restrict file permissions:
```
chmod 600 ~/.msmtprc
```
Important: Use a Gmail App Password instead of your real password.

# Build and Run the Docker Container
Build the Image
```
docker build -t otp_scraper
```
Run the Container
```
docker run -it --rm -v "$(pwd)/series_numbers.txt:/app/series_numbers.txt" otp_scraper
```

# Automate with PowerShell + Task Scheduler
Run Manually
```
powershell -ExecutionPolicy Bypass -File automation/nyeremenybetet-idozito.ps1
```

Schedule the Task, Open Task Scheduler, Create a New Task, Trigger: Run Daily or Weekly, Action: Start a Program → powershell.exe
Arguments:
```
-ExecutionPolicy Bypass -File C:\Path\To\automation\nyeremenybetet-idozito.ps1
```
