#!/bin/bash

# Configuration
TXT_FILE="series_numbers.txt"
LOG_FILE="gepkocsinyeremeny_results.txt"
EMAIL_SUBJECT="Car Lottery Deposit Results"
TO_EMAIL="your-email@gmail.com"
GMAIL_USER="your-email@gmail.com"
PASS_FILE="/etc/passwd"

# Reading the series numbers from a file
if [[ -f "$PASS_FILE" ]]; then
    GMAIL_PASS=$(cat "$PASS_FILE")
else
    echo "[ERROR] Password file not found"
    exit 1
fi

# Check if the series numbers file exists
if [[ ! -f "$TXT_FILE" ]]; then
    echo "[ERROR] Series numbers file not found: $TXT_FILE"
    exit 1
fi

declare -A series_numbers

mapfile -t SERIES_ARRAY < "$TXT_FILE"

echo "[DEBUG] Series Numbers Read: ${SERIES_ARRAY[@]}"

echo "[INFO] Running the script for the following series-number pairs:"
for pair in "${SERIES_ARRAY[@]}"; do
    echo "Series-Number: $pair"
done

echo "[INFO] Executing Python script for each pair..."
for pair in "${SERIES_ARRAY[@]}"; do
    python3 /app/gepkocsi_betet.py "$pair"
    EXIT_CODE=$?

    if [[ $EXIT_CODE -ne 0 ]]; then
        echo "[ERROR] Python script failed for pair: $pair. Check $LOG_FILE for details."
    else
        echo "[SUCCESS] Python script executed successfully for: $pair"
    fi
done

echo "[INFO] All series-number pairs processed."

# Send email with results
if [[ -f "$LOG_FILE" ]]; then
    echo "[INFO] Sending results via email..."
    EMAIL_CONTENT="Here are your car lottery deposit results:
$(cat $LOG_FILE)"
    echo -e "Subject: $EMAIL_SUBJECT\n\n$EMAIL_CONTENT" | msmtp --debug --from="$GMAIL_USER" -t "$TO_EMAIL"
    echo "[INFO] Email sent successfully to $TO_EMAIL."
else
    echo "[ERROR] Log file not found, email not sent."
fi

exit 0
