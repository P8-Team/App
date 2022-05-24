# App

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=P8-Team_App&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=P8-Team_App)

## Running the program

### Requirements
- Be on a native install of Linux
- airmon-ng
- tshark
- python 3.10
- Install packages in requirements.txt (`pip install -r requirements.txt`)
- 3 wireless adapters connected and configured in config.yml

### Setting the wireless adapters to monitormode

```bash
sudo airmon-ng start wlan0 <channel>
```

### Run the listener

```bash
python3 src.run.listen_classifier.py
```

