import socket
import timing
import os
from threading import Thread
import requests

resolved = {}


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


def sticky_port():
    ctep = input('Please type in the country name or the country code' + '\n')
    with open('Sticky_port.txt', 'r') as s:
        with open('sticky.txt', 'a') as o:
            o.writelines(x for x in s.readlines() if ctep in x)
    print('Saved the ports you want.')
    exit()


def per_request_port():
    ctep = input('Please type in the country name or the country code' + '\n')
    with open('PerRequest_port.txt', 'r') as s:
        with open('per_request.txt', 'a') as o:
            o.writelines(x for x in s.readlines() if ctep in x)
    print('Saved the ports you want.')


def domain_ip():
    ps = input('Please enter the domain you want to convert to IP' + '\n')
    result = socket.gethostbyname(ps)
    print('The IP address for this hostname is: ' + repr(result))
    rep = input('Do you want to save the the result to file? y/n' + '\n')
    if rep == 'y':
        with open('ip_address.txt', 'a') as ri:
            ri.writelines(result + '\n')
    print('Saved the requested IP address')


def get_ip(host):
    hostname = host.split(":")[0]
    full_address = lambda x: resolved[hostname] + ":" + x.split(":")[1]
    lookup = lambda x: requests.get("https://dns-api.org/A/" + x.rstrip(), verify=True).json()
    if hostname not in resolved:
        ip = lookup(hostname)[0]["value"]
        resolved[hostname] = ip
    return full_address(host)


def domain_ip_bulk():
    ctep = input('Do you want to convert Sticky ports or Per Request ports? stick/per' + '\n')
    if ctep == 'stick':
        with open('sticky_port.txt', 'r') as s:
            with open('stick_ip_address.txt', 'a') as ri:
                data = [i for i in s.readlines()]
                threads = [ThreadWithReturnValue(target=get_ip, args=(x,)) for x in data]
                print("Working...")
                start = [x.start() for x in threads]
                ri.writelines(x.join() for x in threads)

    if ctep == 'per':
        with open('PerRequest_port.txt', 'r') as s:
            with open('per_req_ip_address.txt', 'a') as ri:
                data = [i for i in s.readlines()]
                threads = [ThreadWithReturnValue(target=get_ip, args=(x,)) for x in data]
                print("Working...")
                start = [x.start() for x in threads]
                ri.writelines(x.join() for x in threads)

while True:
    print('SmartProxy Endpoint Generator v1.0')
    print('Coded by JBusiness')
    print('Enter V to view country codes')
    print('Enter 1 to generate Sticky Ports')
    print('Enter 2 to generate Per Request Ports')
    print('Enter 3 to convert domain proxy to IP proxy')
    print('Enter 4 to convert domain proxy to IP proxy in Bulk')
    picky = input('Which option you want to choose?' + '\n')
    if picky == 'v':
        os.system('notepad.exe country_code.txt')
    if picky == '1':
        sticky_port()
    if picky == '2':
        per_request_port()
    if picky == '3':
        domain_ip()
    if picky == '4':
        domain_ip_bulk()
