#! /usr/bin/env python3


from bs4 import BeautifulSoup
import colorama as cr
from getpass import getpass
import math
import os
import pexpect as px
from PIL import Image
import pytesseract
import re
import requests
import subprocess
import sys
import webbrowser as wb
import zipfile as zp

introAscii = """
                        @@@@@@@@@@@@@@
           @            @@@@@@@@@@@@@@
         @@@@                @@@
        @@@@@                @@@    @@@@@@
       @@@ @@    @@@     @@  @@@   @@@@@@@@
      @@@   @@   @@@     @@  @@@  @@@    @@@
     @@@    @@  @@@      @@@ @@@ @@@      @@
    @@@     @@  @@@      @@@ @@  @@       @@
    @@@     @@  @@@      @@@ @@ @@@       @@
   @@@      @@  @@       @@ @@@ @@        @@
  @@@@@@@@@@@@  @@       @@ @@@ @@        @@
  @@@@@@@@@@@@ @@@      @@@ @@@ @@        @@
 @@@@      @@@ @@@      @@@ @@@ @@        @@
 @@@       @@@ @@@     @@@  @@  @@       @@@
 @@@       @@@ @@@     @@@  @@  @@       @@
 @@@       @@@ @@@   @@@@        @@     @@@
@@@        @@@  @@@@@@@@         @@@   @@@
 @@        @@@  @@@@@@@           @@@@@@@
              @@  @@@   @@  @@@    @@@
              @@        @@ @@@@@@@@        @@        @
              @@@       @@ @@@@@@@@@@      @@@      @@@
              @@@      @@@    @@  @@@@@   @@@@@     @@
               @@      @@@   @@@    @@@@  @@@@@     @@
               @@      @@    @@@     @@@  @@ @@@    @@
               @@@    @@@ @@@@@       @@@@@@ @@@    @@
                @@    @@@ @@@@@       @@ @@@  @@@  @@@
                @@   @@@   @@@@@@@@@@@@@ @@   @@@  @@@
                @@@  @@   @@@@@@@@@@@@@  @@    @@  @@@
                @@@ @@@  @@@      @@    @@@    @@@ @@
                @@@@@@   @@             @@@    @@@ @@
                 @@@@   @@@             @@@     @@@@@
                 @@@@   @@              @@@     @@@@
                 @@@                    @@       @@@
                  @                     @@       @@
                                        @@                Created by: KemoSabe
"""


def get_vpn_login_info():
    #  This function gathers the current username and password from \
    #  vpnbook.com and returns them
    print(cr.Fore.GREEN + '\n...........................\n')
    print(cr.Fore.YELLOW + "Trying to obtain current Username and Password.")
    try:
        #  Attempt to gain login information
        print('Connecting to vpnbook.com...')
        r = requests.get(URL, headers=HEADER)
        soup = BeautifulSoup(r.content, 'html.parser')
        print('Parsing data...')
        user = ''
        paswd = ''
        all_strong = soup.find_all('strong')
        img_count = 0
        for txt in all_strong:
            if txt.text[:4] == 'User':
                if user == '':
                    user = txt.text.replace('Username: ', '')
                    print(cr.Fore.GREEN + 'Current Username obtained!!')
            if txt.text[:4] == 'Pass':
                if img_count == 0:
                    image_php = txt.img['src']
                    # image_url = f'{URL}/{image_php}'
                    image_request = requests.get(f'{URL}/{image_php}', headers=HEADER).content
                    with open('pass_image.png', 'wb') as f:
                        f.write(image_request)
                    img_count += 1
                    if paswd == '':
                        paswd = image_handle('pass_image.png')
        print(cr.Fore.GREEN + '\n...........................\n')
        return user, paswd
    except:
        # Allows user to manually obtain VPN login information
        print(cr.Fore.RED + "Unable to obtain Username and Password!")
        print(cr.Fore.YELLOW
              + "You can manually obtain Username and Password.")
        manual_try_vpn = input("Would you like to try manually? (y/n)")
        if manual_try_vpn == 'y':
            print('Opening '
                  + cr.Fore.BLUE + URL + cr.Style.RESET_ALL
                  + ' ...')
            #  Opens browser to obtain username and password
            wb.open(URL)
            #  Manual username and password inputs
            print(cr.Fore.YELLOW + "What is the Username?")
            manual_user = input(">> ")
            print(cr.Fore.YELLOW + "What is the Password?")
            manual_paswd = input(">> ")
            print(cr.Fore.GREEN + '\n\n...........................\n')
            return manual_user, manual_paswd
        else:
            sys.exit()


def connect_to_vpn(username, password, country, country_number, protocol,
                   port):
    #  This function connects user to VPN
    #  Dictionary used during confirmation in human readable form
    c_check = {'us': 'US', 'euro': 'European', 'ca': 'Canada',
               'de23': 'Germany'}
    cn_check = {'1': 'Primary', '3': 'Primary', '2': 'Backup'}
    p_check = {'tcp': 'TCP', 'udp': 'UDP'}
    port_check = port
    #  This confirms user selection:
    print(cr.Fore.CYAN + '\n\n...........................\n')
    print('Country is ' + cr.Fore.CYAN + '{}.'.format(c_check[country]))
    print('Connection will be on the  ' + cr.Fore.CYAN +
          '{} server.'.format(cn_check[country_number]))
    print('Protocol is  ' + cr.Fore.CYAN + '{}.'.format(p_check[protocol]))
    print('Port is  ' + cr.Fore.CYAN + '{}.'.format(port_check))
    print(cr.Fore.CYAN + '\n...........................\n')
    last_chance = input(cr.Fore.CYAN + 'Is this information correct? (y/n) ')
    if last_chance == 'n':
        quit()
    VPN = 'vpnbook-{}{}-{}{}.ovpn'.format(country, country_number, protocol,
                                          port)
    #  Prints user selection information
    print(cr.Fore.BLUE + '\n\n...........................\n')
    print(cr.Fore.BLUE + 'Connecting to VPN server on ' + VPN)
    print(cr.Fore.YELLOW + "Use Ctrl-C to exit.")
    print()
    print(cr.Fore.GREEN + 'VPN Username=%s and VPN Password=%s' % (username,
                                                                   password))
    #  Spawns connection to VPN
    try:
        sudo_passwd = getpass('Enter your sudo password: ')  # Protects pswd
        child = px.spawnu('sudo', ['openvpn', '--auth-nocache', '--config',
                                   VPN])
        child.waitnoecho()
        child.sendline(str(sudo_passwd))
        child.waitnoecho()
        child.sendline(username)
        child.waitnoecho()
        child.sendline(password)
        child.logfile = sys.stdout  # Prints connection information
        child.expect(px.EOF, timeout=None)
        child.interact()
    except KeyboardInterrupt:
        print(cr.Fore.RED
              + '\n\n\n\nYou have quit! You are no longer in a VPN.')
    finally:
        print('\nEnter sudo password to teminate VPN')
        subprocess.call(['sudo', 'kill', str(child.pid)])
        sys.exit()


def quit():
    #  Determines if user wants to quit:
    quit_choice = input(cr.Fore.RED + '\nWould you like to quit? (y/n) ')
    if quit_choice == 'n':
        main()
    else:
        sys.exit()

def image_handle(image, canvas_width=110, canvas_height=30):
    white = (255,255,255)
    image2 = 'pass_image_resized.png'

    im = Image.open(image)

    original_width, original_height = im.size
    x1 = int(math.floor((canvas_width - original_width) / 2))
    y1 = int(math.floor((canvas_height - original_height) / 2))

    new_image = Image.new("RGB", (canvas_width, canvas_height), white)
    new_image.paste(im, (x1, y1, x1 + original_width, y1 + original_height))
    new_image.save(image2)

    im2 = Image.open(image2)
    text = pytesseract.image_to_string(im2, config='')
    print(cr.Fore.GREEN + 'Current Password obtained!!')
    return text

def check_dir(directory):
    #  This checks to see if certificate bundle directory exits
    if not os.path.exists(directory):
        print('Making directory ' + directory)
        os.makedirs(directory)
        download_extract(directory)
        print('Great! You can now use VPN_connect.py')
    else:
        download_extract(directory)
        print('Great! You can now use VPN_connect.py')


def download_zip_file(file_url, file_name, directory):
    #  This downloads the certificate bundle zip files
    os.chdir(directory)
    print('Downloading ' + file_name)
    r = requests.get(file_url)
    with open(file_name, 'wb') as vpn_file_dwnld:
        vpn_file_dwnld.write(r.content)


def extract_zip_file(zipfile, directory):
    #  This will extract certificate bundle zip files
    with zp.ZipFile(zipfile, 'r') as ext_zip:
        print('Extracting ' + zipfile)
        print()
        ext_zip.extractall(path=directory)
        ext_zip.close()


def download_extract(directory):
    #  This will scrape certificate bundles
    vpn_files_url = []
    print('Connecting to vpnbook.com...')
    r = requests.get(URL, headers=HEADER)
    soup = BeautifulSoup(r.content, 'html.parser')
    print('Parsing data...')
    zip_links = soup.find_all('a', href=re.compile('zip'))
    for link in zip_links:
        temp_name = link.get('href')[22:]
        vpn_files_url.append(temp_name)

    for partUrl in vpn_files_url:
        file_url = URL + '/free-openvpn-account/' + partUrl
        file_name = partUrl
        download_zip_file(file_url, file_name, directory)
        extract_zip_file(file_name, directory)


def main():
    #  Attempts to gain current VPN login information
    # username, password = get_vpn_login_info()
    print('Username is ' + cr.Fore.BLUE + USERNAME + cr.Style.RESET_ALL +
          ' and Password is ' + cr.Fore.BLUE + PASSWORD
          + cr.Style.RESET_ALL + '.')
    #  Determines what country the user wants to use:
    print("\nWould you like to use a US server or other?\
          \nEnter 'u' for US server.\
          \nEnter 'o' for other.")
    print(cr.Fore.YELLOW + "Use Europe for more anonymity.")
    country_choice = input(">> ")
    if country_choice == 'u':
        country = 'us'
    elif country_choice == 'o':
        print("\nThe following are the other servers:")
        print("\n----------------\
              \nEnter 'e' for Europe.\
              \nEnter 'g' for Germany.\
              \nEnter 'c' for Canada.\
              \n----------------")
        other_country_choice = input('What other server would you like to use?\
                                     >> ')
        if other_country_choice == 'e':
            country = 'euro'
        elif other_country_choice == 'g':
            print(cr.Fore.YELLOW + 'Germany only has a primary server.')
            country = 'de23'
        elif other_country_choice == 'c':
            print(cr.Fore.YELLOW + 'Canada only has a primary server.')
            country = 'ca'
        else:
            quit()
    else:
        quit()
    #  Allows user to choose primary or Backup server:
    print("\nWould you like to connect to Primary server or Backup server?\
          \nEnter 'p' for Primary\
          \nEnter 'b' for Backup")
    serv_choice = input(">> ")
    if serv_choice == 'p':
        if country == 'de23':
            country_number = '3'
        else:
            country_number = '1'
    elif serv_choice == 'b':
        if country == 'de23' or country == 'ca':
            print(cr.Fore.RED
                  + "Your current country doesn't have a Backup server.\n")
            quit()
        else:
            country_number = '2'
    else:
        quit()
    #  Determines what protocol the user wants:
    print("\nWould you like to use TCP or UDP?\
          \nEnter 't' for TCP\
          \nEnter 'u' for UDP")
    print(cr.Fore.YELLOW
          + "TCP has less data errors but it is slightly slower.")
    protocol_choice = input(">> ")
    if protocol_choice == 't':
        protocol = 'tcp'
    elif protocol_choice == 'u':
        protocol = 'udp'
    else:
        quit()
    #  Determines what port the user wants:
    if protocol == 'tcp':
        print("\nWhich port do you want to use?\
        \nEnter '1' for port 80\
        \nEnter '2' for port 443")
        tcp_choice = input(">> ")
        if tcp_choice == '1':
            port_choice = '80'
        elif tcp_choice == '2':
            port_choice = '443'
        else:
            quit()
    else:
        print("\nWhich port do you want to use?\
        \nEnter '1' for port 53\
        \nEnter '2' for port 25000")
        udp_choice = input(">> ")
        if udp_choice == '1':
            port_choice = '53'
        elif udp_choice == '2':
            port_choice = '25000'
        else:
            quit()
    #  Connects to VPN with selected input
    connect_to_vpn(USERNAME, PASSWORD, country, country_number, protocol,
                   port_choice)


#  Initialization and main::
if __name__ == '__main__':
    cr.init(autoreset=True)
    URL = 'http://www.vpnbook.com'
    HEADER = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
         AppleWebKit/537.36 (KHTML, like Gecko)\
         Chrome/55.0.2869.0 Safari/537.36',
    }
    USERNAME = ''
    PASSWORD = ''
    #  Introduction
    print('\n' + introAscii)
    print("\nWelcome to a free VPN connection tool!\
          \nThis tool will connect you to a VPN server.\n")
    #  The certificate bundles have to be downloaded and extracted in the same
    #  folder as this code.
    certs_conf = input("Do you have the certificate bundles? (y/n) ")
    if certs_conf == 'n':
        print(cr.Fore.YELLOW
              + '\nCertificates must be in the same directory as this tool.'
              + cr.Style.RESET_ALL)
        print('Your current Directory is:')
        print(cr.Fore.GREEN + os.getcwd())
        print(cr.Fore.YELLOW
              + '\nDo you want to use this directory path? (y/n)')
        current_dir = input('>> ')
        if current_dir == 'y':
            directory = str(os.getcwd())
        elif current_dir == 'n':
            #  The full path has to be used or the code will create
            #  sub directories. CAN NOT use "."!
            print('\n\nWhat is the '
                  + cr.Fore.RED + 'FULL'
                  + cr.Style.RESET_ALL
                  + ' path that you want your cert bundles stored at?')
            directory = input('>> ')
        else:
            sys.exit()
        check_dir(directory)
        USERNAME, PASSWORD = get_vpn_login_info()
        main()
    elif certs_conf == 'q':
        sys.exit()
    else:
        USERNAME, PASSWORD = get_vpn_login_info()
        main()
