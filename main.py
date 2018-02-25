import control
import config
from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)

@app.route('/')
def index():
    uptime = control.system_status()
    mode = control.check_mode()
    tor_status = control.check_tor()
    proxy_status = control.check_3proxy()
    dnsproxy_status = control.check_dnsproxy()
    vwdial_status = control.check_wvdial()
    return render_template('index.html',uptime=uptime,mode=mode,tor_status=tor_status,proxy_status=proxy_status,dnsproxy_status=dnsproxy_status,vwdial_status=vwdial_status)

@app.route('/wifi/edit', methods=['GET', 'POST'])
def wifi_edit():
    f = open(config.hostapd_conf, 'r').read()
    if request.method == "POST" :
        wifiedit = request.form['wifiedit']
        f = open(config.hostapd_conf, 'w').write(wifiedit)
        control.restart_hostapd()
        return redirect(url_for('wifi_edit'))
    return render_template('wifi.html', hostapd_conf=f)

@app.route('/3g/edit', methods=['GET', 'POST'])
def wvdial_edit():
    f = open(config.wvdial_conf, 'r').read()
    if request.method == "POST" :
        wvdialedit = request.form['wvdialedit']
        f = open(config.wvdial_conf, 'w').write(wvdialedit)
        control.restart_wvdial()
        control.restart_dnsproxy()
        return redirect(url_for('wvdial_edit'))
    return render_template('3g.html', wvdial_conf=f)

@app.route('/dns/update', methods=['GET', 'POST'])
def dns_edit():
    f = open(config.dns_conf, 'r').readline()
    if request.method == "POST":
        dns_update = request.form['dnsupdate']
        f = open(config.dns_conf, 'w').writelines(dns_update + '\n' + dns_update + '\n' + dns_update + '\n' + dns_update + '\n' + dns_update)
        control.restart_dnsproxy()
        return redirect(url_for('dns_edit'))
    return render_template('dns_proxy.html', dns_update=f)

@app.route('/socks/edit', methods=['GET', 'POST'])
def socks_edit():
    conf = ['internal 192.168.22.1','daemon', 'plugin /lib/3proxy/TransparentPlugin.ld.so transparent_plugin', 'flush','auth iponly','allow * * * *','parent 1000 socks5 127.0.0.1 9050','tcppm -i192.168.22.1 6666 127.0.0.1 11111']
    conf2 = ['internal 192.168.22.1', 'daemon', 'plugin /lib/3proxy/TransparentPlugin.ld.so transparent_plugin', 'flush','auth iponly', 'allow * * * *','tcppm -i192.168.22.1 6666 127.0.0.1 11111']
    if request.method == 'POST' and request.form['workmode'] == '3':
        socks_ip = request.form['tsocksa_ip']
        socks_port = request.form['tsocksa_port']
        socks_login = request.form['tsocksa_lg']
        socks_pass = request.form['tsocksa_pw']
        conf.insert(0,'#3')
        conf.insert(8,'parent 1000 socks5 ' + socks_ip + ' ' + socks_port + ' ' + socks_login + ' ' + socks_pass)
        control.save_proxy_cfg(conf)
        control.restart_3proxy()
    elif request.method == 'POST' and request.form['workmode'] == '2':
        socks_ip = request.form['tsocks_ip']
        socks_port = request.form['tsocks_port']
        conf.insert(0,'#2')
        conf.insert(8,'parent 1000 socks5 ' + socks_ip + ' ' + socks_port)
        control.save_proxy_cfg(conf)
        control.restart_3proxy()
    elif request.method == 'POST' and request.form['workmode'] == '1':
        conf.insert(0, '#1')
        control.save_proxy_cfg(conf)
        control.restart_3proxy()
    elif request.method == 'POST' and request.form['workmode'] == '4':
        socks_ip = request.form['tsocks_ip']
        socks_port = request.form['tsocks_port']
        conf2.insert(0,'#4')
        conf2.insert(7,'parent 1000 socks5 ' + socks_ip + ' ' + socks_port)
        control.save_proxy_cfg(conf2)
        control.restart_3proxy()
    elif request.method == 'POST' and request.form['workmode'] == '5':
        socks_ip = request.form['tsocksa_ip']
        socks_port = request.form['tsocksa_port']
        socks_login = request.form['tsocksa_lg']
        socks_pass = request.form['tsocksa_pw']
        conf2.insert(0,'#5')
        conf2.insert(7,'parent 1000 socks5 ' + socks_ip + ' ' + socks_port + ' ' + socks_login + ' ' + socks_pass)
        control.save_proxy_cfg(conf2)
        control.restart_3proxy()

    return render_template('socks.html')

@app.route('/system/reboot')
def reboot():
    control.reboot_router()

@app.route('/3g/restart')
def restart_3g():
    wvdial_restart = control.restart_wvdial()
    return render_template('success.html', wvdial_restart=wvdial_restart)

if __name__ == '__main__':
    app.run(host='0.0.0.0')