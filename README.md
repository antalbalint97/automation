# Overview
This repository contains automation scripts designed to run various tasks, including web scraping, scheduling jobs, and email notifications.

Currently, it includes
- the OTP Gépkocsinyeremény Scraper, which scrapes the OTP Gépkocsinyeremény website using Selenium, running inside a Docker container where a Bash script executes a Python script to process data. It reads series_numbers from a .txt file, logs the results, and sends email notifications via msmtp using a Gmail App Password. The entire workflow is fully automated with PowerShell and Windows Task Scheduler for seamless execution.
