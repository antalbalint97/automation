# 🚀 Automation Project
This repository contains automation scripts designed to run various tasks, including web scraping, scheduling jobs, and email notifications.

Currently, it includes the OTP Gépkocsinyeremény Scraper, which:

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
 │── automation               # Mail sending client & Task Scheduler Powershell code
 │   ├── nyeremenybetet-idozito.ps1
 │   ├── msmtprc
 │── README.md
 │── .gitignore
```
