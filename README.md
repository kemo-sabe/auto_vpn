# ABOUT
This is a simple python script that connects a user to a vpn server. The vpn service that is used for this script is vpnbook.com. 

## About VPNBOOK

- Built for performance
- No port or website restrictions
- Strong AES-256, AES-128 encryption
- No bandwidth limits
- Network Integrity
- Anonymity (No traffic stored, only your IP and time. Logs are automatically removed every week.)

---

# Installation
1. Install required libraries.
2. "cd" into desired directory.
2. Clone this repository.
`git clone https://github.com/kemo-sabe/auto_vpn`
3. After clone:
`chmod +x vpn_connect.py`

---

# Additional information
This script is built with the following settings/prerequisites in mind:

- PYTHON 3 (PYTHON 3.5.2 was used during coding/testing)
- 64-bit LINUX SYSTEM (tested on UBUNTU and MANJARO)
- VPN USERNAME and PASSWORD is scrapped off website and is subject to change depending on website redesign.

---

## PYTHON Library Information

### Third Party Libraries 

**Must be installed for the script to work!**

- requests
- bs4
- lxml
- colorama
- selenium (version > 3.4)
>"Selenium requires a driver to interface with the chosen browser. Firefox, for example, requires geckodriver, which needs to be installed before the below examples can be run. Make sure it’s in your PATH, e. g., place it in /usr/bin or /usr/local/bin." -pypi documentation

[Click here to see the latest geckodriver releases](https://github.com/mozilla/geckodriver/releases)

[geckodriver version 16.0](https://github.com/mozilla/geckodriver/releases/download/v0.16.0/geckodriver-v0.16.0-win64.zip)


To install these libraries using pip:

`sudo pip3 install selenium`
`sudo pip3 install requests`
`sudo pip3 install bs4`
`sudo pip3 install colorama`
`sudo pip3 install lxml`

---

### PYTHON Standard Libraries Used

- sys
- getpass
- pexpect
- os
- signal
- subprocess
- urllib.request
- zipfile

---
	
**PLEASE CONTRIBUTE ANY ADDITIONS/SUGGESTIONS TO THE CODE. IF IT IS USEFUL, PAY IT FORWARD.**
