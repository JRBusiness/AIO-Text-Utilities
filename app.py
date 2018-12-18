import socket
import timing
from threading import Thread
import requests

resolved = {}


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


def url_dup_re():
    host = [d.rstrip('/') for d in open('url_input.txt', 'r', encoding='utf8').readlines()]
    with open('url_output.txt', 'a') as r:
        r.writelines(set(repr.join(i) for i in host))


def sticky_port():
    ctep = input('Please type in the country name or the country code' + '\n')
    with open('./Sticky_port.txt', 'r') as s:
        with open('sticky.txt', 'a') as o:
            data = [i for i in s.readlines()]
            ctep_exist = [x for x in data if ctep in x]
            o.writelines(x for x in ctep_exist)
    print('Saved the ports you want.')


def per_request_port():
    ctep = input('Please type in the country name or the country code' + '\n')
    with open('./PerRequest_port.txt', 'r') as s:
        with open('per_request.txt', 'a') as o:
            data = [i for i in s.readlines()]
            ctep_exist = [x for x in data if ctep in x]
            o.writelines(x for x in ctep_exist)
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
        with open('./sticky_port.txt', 'r') as s:
            with open('stick_ip_address.txt', 'a') as ri:
                data = [i for i in s.readlines()]
                threads = [ThreadWithReturnValue(target=get_ip, args=(x,)) for x in data]
                print("Working...")
                start = [x.start() for x in threads]
                ri.writelines(x.join() for x in threads)

    if ctep == 'per':
        with open('./PerRequest_port.txt', 'r') as s:
            with open('per_req_ip_address.txt', 'a') as ri:
                data = [i for i in s.readlines()]
                threads = [ThreadWithReturnValue(target=get_ip, args=(x,)) for x in data]
                print("Working...")
                start = [x.start() for x in threads]
                ri.writelines(x.join() for x in threads)


while True:
    print('You are using The Revolution Utilities by JM Revolution')
    print('Please choose one of the following options by entering the option number:')
    print('Which ')
    print('1 - Duplicated Url Remover')
    print('2 - Convert Domain DNS to IP Address')
    print('2 - Convert a list of Domain DNS to IP Address')
    ur = input()
    if ur == 'jmr':
        mk = input('Enter the Admin password to unlock full features')
        if mk == 'Alibaba.1408':
            print('SlChoose one of the following options:')
            print('1 - Get Smartproxy Sticky proxy')
            print('2 - Get Smartproxy Per Request proxy')
            cc = input()
            if cc == '1':
                sticky_port()
            if cc == '2':
                per_request_port()
    if ur == '1':
        url_dup_re()
    if ur == '2':
        domain_ip()
    if ur == '3':
        domain_ip_bulk()
