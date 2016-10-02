#! /usr/bin/env python3


import sys, requests, signal, subprocess, os
import urllib.request
from bs4 import BeautifulSoup
from getpass import getpass
import pexpect as px
import colorama as cr
import zipfile as zp

def get_vpn_login_info():
    #  This function gathers the current username and password from vpnbook.com and returns them
    print(cr.Fore.YELLOW + "Trying to obtain current Username and Password.")
    try:
        #  First attempt to gain information
        url = "http://www.vpnbook.com/freevpn"
        print('Connecting to vpnbook.com...')
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'xml')
        print('Parsing data...')
        findBox = soup.find_all('div', {'class': 'one-third column box light featured'})
        for box in findBox:
            user = box.find_all('li')[7].text.replace('Username: ', '')
            paswd = box.find_all('li')[8].text.replace('Password: ', '')
            print(cr.Back.GREEN + 'Current Username and Password obtained!!')
            return user, paswd
    except:
        #  Second attempt to gain information on different page because the first attempt failed
        print(cr.Back.RED + "Unable to obtain Username and Password. :`(")
        try_alt_way = input("Would you like to try another way? (y/n) ")
        if try_alt_way == 'n':
            sys.exit()
        else:
            try:
                url_alt = 'http://www.vpnbook.com'
                print('Connecting to vpnbook.com...')
                r = requests.get(url_alt)
                soup = BeautifulSoup(r.content, 'xml')
                print('Parsing data...')
                find_div_class_row = soup.find_all('div', {'class': 'row'})
                li_dict = {}
                for row in find_div_class_row:
                    find_li_id_openvpn = soup.find_all('li', {'id': 'openvpn'})
                    for li in find_li_id_openvpn:
                        if 'user_alt' not in li_dict:
                            li_dict['user_alt'] = li.find_all('li')[7].text.replace('Username: ', '')
                        if 'paswd_alt' not in li_dict:
                            li_dict['paswd_alt'] = li.find_all('li')[8].text.replace('Password: ', '')
                if 'user_alt' in li_dict and 'paswd_alt' in li_dict:
                    print(cr.Back.GREEN + 'Current Username and Password obtained!!')
                    return li_dict['user_alt'], li_dict['paswd_alt']
            except:
                #  The first and second attempts failed. The Username and Password are obtained manually.
                print(cr.Back.RED + "Still unable to obtain Username and Password!")
                print(cr.Back.YELLOW + "You can manually go to vpnbook.com to obtain Username and Password.")
                manual_try_vpn = input("Would you like to try manually? (y/n)")  #  Allows user to manually obtain VPN login information
                if manual_try_vpn == 'y':
                    print(cr.Back.YELLOW + "What is the Username?")
                    manual_user = input(">> ")
                    print(cr.Back.YELLOW + "What is the Password?")
                    manual_paswd = input(">> ")
                    return manual_user, manual_paswd
                else:
                    sys.exit()


def connect_to_vpn(username, password, country, country_number, protocol, port):
    #  This function connects user to VPN
    #  Dictionary used during confirmation in human readable form
    c_check = {'us': 'US', 'euro': 'European','ca':'Canada', 'de23': 'Germany'}
    cn_check = {'1': 'Primary', '3': 'Primary', '2': 'Backup'}
    p_check = {'tcp': 'TCP', 'udp': 'UDP'}
    port_check = port
    #  This confirms user selection:
    print(cr.Fore.CYAN +'\n\n...........................\n')
    print('Country is ' + cr.Back.CYAN + '{}.'.format(c_check[country]))
    print('Connection will be on the  ' + cr.Back.CYAN + '{} server.'.format(cn_check[country_number]))
    print('Protocol is  ' + cr.Back.CYAN + '{}.'.format(p_check[protocol]))
    print('Port is  ' + cr.Back.CYAN + '{}.'.format(port_check))
    print(cr.Fore.CYAN +'\n...........................\n')
    last_chance = input(cr.Fore.CYAN + 'Is this information correct? (y/n) ')
    if last_chance == 'n':
        quit()
    VPN = 'vpnbook-{}{}-{}{}.ovpn'.format(country, country_number, protocol, port)
    #  Prints user selection information
    print(cr.Fore.BLUE + '\n\n...........................\n')
    print(cr.Fore.BLUE + 'Connecting to VPN server on ' + VPN)
    print(cr.Back.YELLOW + "Use Ctrl-C to exit.")
    print()
    print(cr.Back.GREEN + 'VPN Username=%s and VPN Password=%s' %(username,password))
    #  Spawns connection to VPN
    try: 
        sudo_passwd = getpass('Enter your sudo password: ') #  Protects user sudo password
        child = px.spawnu('sudo', ['openvpn', '--config', VPN])
        child.waitnoecho()
        child.sendline(str(sudo_passwd))
        child.waitnoecho()
        child.sendline(username)
        child.waitnoecho()
        child.sendline(password)
        child.logfile = sys.stdout  #  Prints connection information
        child.expect(px.EOF, timeout=None)
        child.interact()
    except KeyboardInterrupt:
        print(cr.Back.RED + '\n\n\n\nYou have quit! You are no longer in a VPN.')
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


def check_dir(directory):
    #  This checks to see if certificate bundle directory exits
    if not os.path.exists(directory):
        print('Making directory ' + directory)
        os.makedirs(directory)
        download_extract(directory)
    else:
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
    url = "http://www.vpnbook.com/freevpn"
    print('Connecting to vpnbook.com...')
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'xml')
    print('Parsing data...')
    findBox = soup.find_all('div', {'class': 'one-third column box light featured'})
    for box in findBox:
        for link in box.find_all('a'):
            urlFile = link.get('href')
            try:
                if len(urlFile) > 30:
                    vpn_files_url.append(urlFile[22:])
            except:
                pass
    for partUrl in vpn_files_url:
            file_url = 'http://www.vpnbook.com/free-openvpn-account/' + partUrl
            file_name = partUrl
            download_zip_file(file_url, file_name, directory)
            extract_zip_file(file_name, directory)


def main():
    #  Attempts to gain current VPN login information
    username, password = get_vpn_login_info()  
    print('Username is ' + cr.Back.YELLOW + username + cr.Style.RESET_ALL + ' and Password is ' + cr.Back.YELLOW  + password + cr.Style.RESET_ALL + '.')
    #  Determines what country the user wants to use:
    print("\nWould you like to use a US server or other?\nEnter 'u' for US server.\nEnter 'o' for other.")
    print(cr.Fore.YELLOW + "Use Europe for more anonymity.")
    country_choice = input(">> ")
    if country_choice == 'u':
        country = 'us'
    elif country_choice == 'o':
        print("\nThe following are the other servers:")
        print("\n----------------\nEnter 'e' for Europe.\nEnter 'g' for Germany.\nEnter 'c' for Canada.\n----------------")
        other_country_choice = input('What other server would you like to use? >> ')
        if other_country_choice == 'e':
            country = 'euro'
        elif other_country_choice == 'g':
            print(cr.Back.YELLOW + 'Germany only has a primary server.')
            country = 'de23'
        elif other_country_choice == 'c':
            print(cr.Back.YELLOW + 'Canada only has a primary server.')
            country = 'ca'
        else:
            quit()     
    else:
        quit()    
    #  Allows user to choose primary or backup server:
    print("\nWould you like to connect to primary server or backup server?\nEnter 'p' for primary or 'b' for backup.")
    serv_choice = input(">> ")
    if serv_choice == 'p':
        if country == 'de23':
            country_number = '3'
        else:
            country_number = '1'
    elif serv_choice == 'b':
        if country == 'de23' or country == 'ca':
            print(cr.Back.RED + "Your current country doesn't have a backup server.\n")
            quit()
        else:
            country_number = '2'
    else:
        quit()
    #  Determines what protocol the user wants:
    print("\nWould you like to use TCP or UDP?\nEnter 't' for TCP or 'u' for UDP.")
    print(cr.Fore.YELLOW + "TCP has less data errors but it is slightly slower.")
    protocol_choice = input(">> ")
    if protocol_choice == 't':
        protocol = 'tcp'
    elif protocol_choice == 'u':
        protocol = 'udp'
    else:
        quit()
    #  Determines what port the user wants:
    if protocol == 'tcp':
        print("\nWhich port do you want to use?\nEnter '80' or '443'.")
        tcp_choice = input(">> ")
        if tcp_choice == '80' or tcp_choice == '443':
            port_choice = tcp_choice
        else:
            quit()
    else:
        print("\nWhich port do you want to use?\nEnter '53' or '25000'.")
        udp_choice = input(">> ")
        if udp_choice == '53' or udp_choice == '25000':
            port_choice = udp_choice
        else:
            quit()
    #  Connects to VPN with selected input
    connect_to_vpn(username, password, country, country_number, protocol, port_choice)  


#  Initialization and main::
if __name__ == '__main__':
    cr.init(autoreset=True)
    #  Introduction
    print("\nWelcome to a free VPN connection tool!\nThis tool will connect you to a VPN server.\n")  
    #  The certificate bundles have to be downloaded and extracted in the same folder as this code.
    certs_conf = input("Do you have the certificate bundles downloaded and unziped? (y/n) ")
    if certs_conf == 'n':
        print(cr.Back.YELLOW + '\nThe certificate bundles should be stored in the same directory as this code.' + cr.Style.RESET_ALL)
        print('Your current Directory is:')
        print(cr.Fore.GREEN + os.getcwd())
        #  The full path has to be used or the code will create sub directories. CAN NOT use "."!
        print('\n\nWhat is the ' + cr.Back.RED + 'FULL' + cr.Style.RESET_ALL + ' path that you want your cert bundles stored at?')
        directory = input('>> ')
        if directory == 'q':
            sys.exit()
        else:        
            check_dir(directory)
            main()
    elif certs_conf == 'q':
        sys.exit()    
    else:
        main()
