import os
import time
import subprocess
import config

def check_tor():
    try:
        tor = subprocess.check_output(['systemctl', 'is-active', 'tor'])
        return 'Active'
    except subprocess.CalledProcessError:
        return 'Down'

def check_3proxy():
    try:
        proxy3 = subprocess.check_output(['systemctl', 'is-active', '3proxy'])
        return 'Active'
    except subprocess.CalledProcessError:
        return 'Down'

def check_dnsproxy():
    try:
        dnsproxy = subprocess.check_output(['systemctl', 'is-active', 'dnsproxy'])
        return 'Active'
    except subprocess.CalledProcessError:
        return 'Down'

def check_wvdial():
    try:
        wvdial = int(subprocess.check_output(["pidof", "-s", "wvdial"]))
        return 'Connected'
    except subprocess.CalledProcessError:
        return 'Down'

def get_pid_wvdial():
    try:
        wvdial = int(subprocess.check_output(["pidof", "-s", "wvdial"]))
        return wvdial
    except subprocess.CalledProcessError:
        return 'none'

def check_mode():
    f = open(config.proxy3_conf,'r').readline().rstrip()
    if f == '#3':
        return 'TOR-SOCKS-AUTH'
    elif f == '#2':
        return 'TOR-SOCKS'
    elif f == '#1':
        return 'TOR Mode'
    else:
        return 'Unknown Mode'

def restart_wvdial():
    if str(get_pid_wvdial()) == 'none':
        run = os.system('wvdial 3G &')
        return 'Success start!!!'
    else:
        os.system('kill -1 ' + str(get_pid_wvdial()))
        time.sleep(10)
        os.system('wvdial 3G &')
        return 'Success restart!!!'

def system_status():
    uptime = subprocess.check_output(["uptime"])
    return str(uptime,'utf-8')

def save_proxy_cfg(conf):
    f = open(config.proxy3_conf, 'w')
    for i in range(len(conf)):
        f.write(conf[i] + "\n")
    f.close()

def restart_3proxy():
    os.system('systemctl stop 3proxy')
    os.system('systemctl start 3proxy')

def restart_dnsproxy():
    os.system('systemctl stop dnsproxy')
    os.system('systemctl start dnsproxy')

def restart_hostapd():
    os.system('systemctl stop hostapd')
    os.system('systemctl start hostapd')