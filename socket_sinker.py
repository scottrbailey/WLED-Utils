import json
import requests
import websocket


class State:
    def __init__(self, on, bri, pal, fx, cols=[]):
        self.on = bool(on)
        self.bri = bri
        self.pal = pal
        self.fx = fx
        self.cols = cols
        self.sx = None
        self.ix = None
        self.ps = None

    def from_json(self, data):
        self.on = bool(data['on'])
        self.bri = data['bri']
        seg = data['seg'][data['mainseg']]
        self.pal = seg['pal']
        self.fx = seg['fx']
        self.sx = seg['sx']
        self.ix = seg['ix']


class Node:
    def __init__(self, name, ip, send, recv):
        self.name = name
        self.ip = ip
        self.send = bool(send)
        self.recv = bool(recv)
        self.state = None
        self.udpport = None


    def from_json(self, data):
        self.name = data['info']['name']
        self.ip = data['info']
        self.udpport = data['info']['udpport']


def scan():
    recv_nodes = []
    send_nodes = []

    if js["state"]["udpn"]["send"]:
        send_nodes.append(ip)
    if js["state"]["udpn"]["recv"]:
        recv_nodes.append(ip)
    nodes = requests.get(f'http://{ip}/json/nodes.json').json()
    for node in nodes['nodes']:
        st = requests.get(f'http://{node["ip"]}/json/state').json()
        if st["udpn"]["recv"]:
            recv_nodes.append(node["ip"])
        if st["udpn"]["send"]:
            send_nodes.append(node["ip"])
    return send_nodes, recv_nodes
        
    
def on_message(ws, message):
    state = json.loads(message)['state']
    if not state["on"]:
        print('Off')
        return    
    seg = state["seg"][0]
    
    if seg["pal"] < 6:
        cols = []
        for col in seg["col"]:
            cv = (col[0] << 16) + (col[1] << 8) + col[2]
            cols.append(f'#{cv:06X}')
        display = f'{fxs[seg["fx"]]} - ({", ".join(cols)})'    
    else:
        display = f'{fxs[seg["fx"]]} - {pals[seg["pal"]]}'
    print(display)
    print(f'Bright: {state["bri"]}  Speed: {seg["sx"]} Intensity: {seg["ix"]}')
    

def on_open(ws):
    ws.send("Connection from Python")
    print("Websocket connection opened")


if __name__ == '__main__':
    # websocket.enableTrace(True)
    ip = '192.168.10.51'
    req = requests.get(f'http://{ip}/json')
    js = req.json()
    send_nodes, recv_nodes = scan()
    fxs = js['effects']
    pals = js['palettes']
    if len(send_nodes) > 0:
        ip = send_nodes[0]
    """    
    ws = websocket.WebSocketApp(f'ws://{ip}/ws', on_open=on_open,
                                on_message=on_message)
    ws.run_forever()
    """
    
