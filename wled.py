import requests
import sys


class Node:
    def __init__(self, ip):
        self.ip = ip
        try:
            req = requests.get(f'http://{ip}/json', timeout=3)
            js = req.json()
        except requests.exceptions.Timeout:
            print(f'Could not to WLED node at {ip}. Configure NODE_IP and try again.')
            sys.exit(1)
        self.state = js['state']
        self.info = js['info']
        self.palettes = js['palettes']
        self.effects = js['effects']
        self.initialize()

    def initialize(self):
        pass

    def win(self, **kwargs):
        query = '&'.join([f'{k.upper()}={v}' for k, v in kwargs.items()])
        req = requests.get(f'http://{self.ip}/win&{query}')

    def live_colors(self):
        req = requests.get(f'http://{self.ip}/json/live')
        return req.json['leds']
