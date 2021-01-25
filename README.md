# Raspberry Pi Presence Light for Teams & Zoom

This project is a fork of [Teams-Presence](https://github.com/maxi07/Teams-Presence), extended to support Zoom using the [Zoom Presence Indicator API](https://github.com/jonathanwelton/zoom-presence-indicator-api).

For simplicity, I kept the indicator light to three colours:

- ![#fa0000](https://via.placeholder.com/15/fa0000/000000?text=+) Red means the user is sharing their screen, i.e. **presenting**
- ![#ff6cb4](https://via.placeholder.com/15/ff6cb4/000000?text=+) Pink means the user is in an active call, i.e. **in a meeting**
- ![#00fa00](https://via.placeholder.com/15/00fa00/000000?text=+) Green means the user is not in a call, i.e. **available**

#### Zoom supported presence statuses

| Status              | Colour                                                          |
| ------------------- | --------------------------------------------------------------- |
| Presenting          | ![#fa0000](https://via.placeholder.com/15/fa0000/000000?text=+) |
| Do not disturb      | ![#ff6cb4](https://via.placeholder.com/15/ff6cb4/000000?text=+) |
| In a calendar event | ![#ff6cb4](https://via.placeholder.com/15/ff6cb4/000000?text=+) |
| In a meeting        | ![#ff6cb4](https://via.placeholder.com/15/ff6cb4/000000?text=+) |
| Available           | ![#00fa00](https://via.placeholder.com/15/00fa00/000000?text=+) |
| Away                | ![#00fa00](https://via.placeholder.com/15/00fa00/000000?text=+) |
| Presence unknown    | ![#0000fa](https://via.placeholder.com/15/0000fa/000000?text=+) |

#### Teams supported presence statuses

| Status                    | Colour                                                          |
| ------------------------- | --------------------------------------------------------------- |
| Presenting                | ![#fa0000](https://via.placeholder.com/15/fa0000/000000?text=+) |
| Busy                      | ![#ff6cb4](https://via.placeholder.com/15/ff6cb4/000000?text=+) |
| Do not disturb            | ![#ff6cb4](https://via.placeholder.com/15/ff6cb4/000000?text=+) |
| In a call                 | ![#ff6cb4](https://via.placeholder.com/15/ff6cb4/000000?text=+) |
| In a conference call      | ![#ff6cb4](https://via.placeholder.com/15/ff6cb4/000000?text=+) |
| In a meeting              | ![#ff6cb4](https://via.placeholder.com/15/ff6cb4/000000?text=+) |
| Urgent interruptions only | ![#ff6cb4](https://via.placeholder.com/15/ff6cb4/000000?text=+) |
| Available                 | ![#00fa00](https://via.placeholder.com/15/00fa00/000000?text=+) |
| Away                      | ![#00fa00](https://via.placeholder.com/15/00fa00/000000?text=+) |
| Be right back             | ![#00fa00](https://via.placeholder.com/15/00fa00/000000?text=+) |
| Inactive                  | ![#00fa00](https://via.placeholder.com/15/00fa00/000000?text=+) |
| Offline                   | ![#00fa00](https://via.placeholder.com/15/00fa00/000000?text=+) |
| Off work                  | ![#00fa00](https://via.placeholder.com/15/00fa00/000000?text=+) |
| Out of office             | ![#00fa00](https://via.placeholder.com/15/00fa00/000000?text=+) |
| Presence unknown          | ![#0000fa](https://via.placeholder.com/15/0000fa/000000?text=+) |

## Features

- Zoom support
- Indicator selector
- Auto-start scripts

## Motivation

This app was created as part of a bigger project to display the presence status of a Zoom user on a Raspberry Pi integrated with a Unicorn pHAT. You can read the original blog post [here](https://jonathanwelton.github.io/2021/01/31/raspberry-pi-presence-light.html).

## Prerequisites

- A Raspberry Pi Zero W with a Unicorn pHAT attached
- Raspbian and Python3 installed on the Pi

## Installation

    git clone https://github.com/jonathanwelton/raspberry-pi-presence-light-for-teams-and-zoom.git
    cd raspberry-pi-presence-light-for-teams-and-zoom
    sudo ./install.sh

## Usage

### Zoom Presence Light

Start by configuring and deploying a version of the [Zoom Presence Indicator API](https://github.com/jonathanwelton/zoom-presence-indicator-api).

Store the configuration values for the API in a config.ini file at the root of this project with the following structure:

[presence_api]
url = **_Zoom Presence Indicator API URL_**
token = **_Zoom Presence Indicator API Verification Token_**

To start the Zoom Presence Indicator, execute:

```
sudo python3 start.py
```

and select option 2, or

```
sudo python3 autoStartZoom.py
```

if you want it to run automatically e.g. when the Pi boots.

### Teams Presence Light

Start by configuring an Azure AD app to access your Teams presence, following <a href="https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app" target="_blank" rel="noopener noreferrer">this guide</a>.

- In the **API permissions** section, add <code>Presence.Read</code>

- In the **Authentication** section, enable <code>Treat application as a public client</code>

- In the **Overview** section, take a note of the <code>Client Id</code> and <code>Tenant Id</code>

To start the Zoom Presence Indicator, execute:

```
sudo python3 start.py
```

and select option 1, or

```
sudo python3 autoStartTeams.py
```

if you want it to run automatically e.g. when the Pi boots.

The first time it runs you will need to provide your Client Id and Tenant Id, and then autheticate.
