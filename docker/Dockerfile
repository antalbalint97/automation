FROM python:3.10-slim

# Update with apt and install everything
RUN apt-get update && apt-get install -y \
    curl unzip wget chromium chromium-driver dos2unix vim \
    bash msmtp msmtp-mta \
    && rm -rf /var/lib/apt/lists/*

# Install python packages like selenium and pytz
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytz

# Moving and copying the scripts
COPY gepkocsi_betet.py /app/gepkocsi_betet.py
COPY run_nyeremenybetet_script_mail.sh /app/run_nyeremenybetet_script_mail.sh
RUN chmod +x /app/run_nyeremenybetet_script_mail.sh
RUN dos2unix /app/run_nyeremenybetet_script_mail.sh
COPY msmtprc /etc/msmtprc
RUN chmod 600 /etc/msmtprc
COPY passwd /etc/ssmtp/passwd

# Beállítjuk az alapértelmezett belépési pontot
ENTRYPOINT ["/bin/bash", "/app/run_nyeremenybetet_script_mail.sh"]
