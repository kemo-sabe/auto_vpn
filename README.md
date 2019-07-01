# ABOUT
This is a simple python script that connects a user to a vpn server. The vpn service that is used for this script is vpnbook.com. A simpler version is being worked on.

## About VPNBOOK

- Built for performance
- No port or website restrictions
- Strong AES-256, AES-128 encryption
- No bandwidth limits
- Network Integrity
- Anonymity (No traffic stored, only your IP and time. Logs are automatically removed every week.)

---

# Installation
1. Install tesseract. This depends on distribution, but an example is
`sudo apt install tesseract-ocr`
1. Clone this repository.
`git clone https://github.com/kemo-sabe/auto_vpn`
2. Install libraries.
`pip install -r requirements.txt`
3. Change script to be executable:
`chmod +x vpn_connect.py`

---

# Additional information
This script is built with the following settings/prerequisites in mind:

- PYTHON 3 (PYTHON 3+ was used during coding/testing)
- 64-bit LINUX SYSTEM (tested on UBUNTU and MANJARO)
- VPN USERNAME and PASSWORD is scrapped off website and is subject to change depending on website redesign.

---

## PYTHON Library Information

### Third Party Libraries

**Must be installed for the script to work!**

- colorama
- bs4
- Pillow
- pytesseract
- requests

---

### PYTHON Standard Libraries Used

- getpass
- math
- os
- pexpect
- re
- signal
- subprocess
- sys
- webbrowser
- zipfile

---

**PLEASE CONTRIBUTE ANY ADDITIONS/SUGGESTIONS TO THE CODE. IF IT IS USEFUL, PAY IT FORWARD.**
