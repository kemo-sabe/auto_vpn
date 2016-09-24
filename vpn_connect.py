#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2016 KemoSabe <kemo_sabe@kemo_sabe>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import sys, requests
from bs4 import BeautifulSoup
from getpass import getpass
import pexpect as px
import colorama as cr

#  Definitions::
def get_vpn_login_info():
    #  This function gathers the current username and password from vpnbook.com and returns them:
    url = "http://www.vpnbook.com/freevpn"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'xml')
    findBox = soup.find_all('div', {'class': 'one-third column box light featured'})
    for box in findBox:
        user = box.find_all('li')[7].text.replace('Username: ', '')
        paswd = box.find_all('li')[8].text.replace('Password: ', '')
        return user, paswd

def country_server():
    #  Determines what country the user wants to use:
    print("Would you like to use a US server or other?\nEnter 'u' for US server.\nEnter 'o' for other.")
    print(cr.Back.YELLOW + "Europe is used for anonymity.")
    country_choice = input(">> ")
    if country_choice == 'u':
        country = 'us'
    elif country_choice == 'o':
        print("The following are the other servers:")
        print(cr.Back.MAGENTA + "\n----------------\nEnter 'e' for Europe.\nEnter 'g' for Germany.\nEnter 'c' for Canada.\n----------------")
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
    return country      

def server_choice(country):
    #  Allows user to choose primary or backup server:
    print("Would you like to connect to primary server or backup server?\nEnter 'p' for primary or 'b' for backup.")
    serv_choice = input(">> ")
    if serv_choice == 'p':
        if country == 'de23':
            country_number = '3'
        else:
            country_number = '1'
    elif serv_choice == 'b':
        if country == 'de23' or country == 'ca':
            print(cr.Back.RED + "Your current country doesn't have a backup server.\n")
            print(cr.Fore.YELLOW + "Would you like to choose a different country? (y/n) ")
            redo_country = input('>> ')
            if redo_country == 'n':
                server_choice(country)
            else:
                main()
        else:
            country_number = '2'
    elif serv_choice == 'q':
        quit()
    return country_number

def protocol_choice():
    #  Determines what protocol the user wants:
    print("\nWould you like to use TCP or UDP?\nEnter 't' for TCP or 'u' for UDP.")
    print(cr.Fore.YELLOW + "TCP has less data errors but slightly slower")
    protocol_choice = input(">> ")
    if protocol_choice == 't':
        protocol = 'tcp'
    elif protocol_choice == 'u':
        protocol = 'udp'
    else:
        quit()
    return protocol
        
def port_choice(protocol):
    #  Determines what port the user wants:
    if protocol == 'tcp':
        print("Which port do you want to use?\nEnter '80' or '443'.")
        tcp_choice = input(">> ")
        if tcp_choice == '80' or tcp_choice == '443':
            port_choice = tcp_choice
        else:
            quit()
    else:
        print("Which port do you want to use?\nEnter '53' or '25000'.")
        udp_choice = input(">> ")
        if udp_choice == '53' or udp_choice == '25000':
            port_choice = udp_choice
        else:
            quit()
    return port_choice

def connect_to_vpn(country, country_number, protocol, port):
    #  Connects user to VPN:
    c_check = {'us': 'US', 'euro': 'European','ca':'Canada', 'de23': 'Germany'}
    cn_check = {'1': 'Primary', '3': 'Primary', '2': 'Backup'}
    p_check = {'tcp': 'TCP', 'udp': 'UDP'}
    port_check = port
    #  This confirms user selection
    print(cr.Fore.CYAN +'\n\n...........................\n')
    print('Country is ' + cr.Back.CYAN + '{}.'.format(c_check[country]))
    print('Connection will be on the  ' + cr.Back.CYAN + '{} server.'.format(cn_check[country_number]))
    print('Protocol is  ' + cr.Back.CYAN + '{}.'.format(p_check[protocol]))
    print('Port is  ' + cr.Back.CYAN + '{}.'.format(port_check))
    print(cr.Fore.CYAN +'\n...........................\n')
    last_chance = input(cr.Fore.YELLOW + 'Is this information correct? (y/n) ')
    if last_chance == 'n':
        quit()
    #  Prints user selection information
    print(cr.Fore.BLUE + '\n\n...........................\n')
    print(cr.Fore.BLUE + 'Connecting to VPN server on vpnbook-{}{}-{}{}.ovpn'.format(country, country_number, protocol, port))
    print(cr.Back.YELLOW + "Use Ctrl-c to exit")
    print()
    print(cr.Back.GREEN + 'VPN Username=%s and VPN Password=%s' %(username,password))
    #  Spawns connection to VPN
    try: 
        sudo_passwd = getpass('Enter your Sudo Password: ') #  Protects User sudo password
        child = px.spawnu('sudo', ['openvpn', '--config', 'vpnbook-us2-tcp80.ovpn'])
        child.waitnoecho()
        child.sendline(str(sudo_passwd))
        child.waitnoecho()
        child.sendline(username)
        child.waitnoecho()
        child.sendline(password)
        child.logfile = sys.stdout  #  Prints connection information
        child.expect(px.EOF, timeout=None)
        child.interact()
    except:
        print(cr.Back.RED + '\n\n\n\nYou have quit! You are no longer in a VPN.')
        child.close()

def quit():
    #  Determines if user wants to quit:
    global looping
    quit_choice = input(cr.Back.RED + '\nWould you like to quit? (y/n) ')
    if quit_choice == 'n':
        main()
    else:
        sys.exit()

def main():
    cs = country_server()                 #  Selects country
    serv = server_choice(cs)              #  Selects server
    prot_c = protocol_choice()            #  Selects protocol
    pc = port_choice(prot_c)              #  Selects Port
    connect_to_vpn(cs, serv, prot_c, pc)  #  Connects to VPN

#  Initialization and main::
if __name__ == '__main__':
    cr.init(autoreset=True)
    print("\nWelcome to a free VPN.\nThis tool will connect you to a VPN.\n")  #  Introduction
    print(cr.Fore.YELLOW + "Trying to obtain current Username and Password.")
    try:
        username, password = get_vpn_login_info()  #  Attempts to gain current VPN login information
        print(cr.Back.GREEN + 'Current Username and Password obtained!!')
    except:
        print(cr.Back.RED + "Unable to obtain Username and Password. :(")
    main()
    sys.exit()
