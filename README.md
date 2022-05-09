# App

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=P8-Team_App&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=P8-Team_App)

## Listening on Wi-Fi

To listen on Wi-Fi, you need to identify the Wi-Fi interfaces that you want to use.

### 1. Identify Wi-Fi interfaces

To list all available Wi-Fi interfaces, run:

```bash
$ sudo iw dev
```

On Windows, run:

```bash
$ netsh wlan show interfaces
```

By now you should have retrieved a list of Wi-Fi interface names.

### 2. Set interfaces to monitor mode

All the interfaces you want to listen to, needs to be set to monitor mode.

Linux:

```bash
$ sudo ifconfig <interface> down
$ sudo iwlist <interface> mode monitor
$ sudo ifconfig <interface> up
```

Windows (Requires [Npcap](https://npcap.com/) and admin privileges):

```bash
$ Wlanhelper.exe <interface> mode monitor
```

Be aware you may not be able to retrieve all frame types, notable data frames, on Windows.

### 3. Start listening

To start listening, run:

```bash
$ python3 src/main.py [...interfaces]
```

For example to listen on interfaces `wlan0` and `wlan1`, run:

```bash
$ python3 src/main.py wlan0 wlan1
```
