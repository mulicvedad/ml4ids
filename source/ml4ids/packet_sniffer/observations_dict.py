import pickle

from datetime import datetime
import sys
print(sys.path)
from packet_sniffer.flow_entry import FlowEntry
from scapy.layers.inet import TCP
from termcolor import colored

DEFAULT_TIMEOUT_SEC = 60


class FlowCollection:
    def __init__(self, dnn_model):
        self.closed_flows = {}
        self.flows = {}
        self.dnn_model = dnn_model
        self.premature_predictions = []

    def add_packet(self, proto, src_ip, src_port, dst_ip, dst_port, packet):
        key1 = (proto, src_ip, src_port, dst_ip, dst_port)
        key2 = (proto, dst_ip, dst_port, src_ip, src_port)

        key = key1

        if key1 in self.flows:
            self.flows[key1].add_fwd(packet)
        elif key2 in self.flows:
            key = key2
            self.flows[key2].add_bwd(packet)
        else:
            self.flows[key1] = FlowEntry()
            self.flows[key1].add_fwd(packet)

        flow = self.flows[key]

        if flow.flow_pkts_num > 20 and flow.flow_pkts_num < 50:
            self.predict_premature(key, flow)

        # If FIN flag is set, move flow from active flows to closed flows
        if (TCP in packet and "F" in packet[TCP].flags) or self.flows[key].timeout:
            self.flows[key].snapshot()
            self.close_flow(key)


    def predict_premature(self, key, flow):
        flow.snapshot()
        is_benign = self.dnn_model.predict(flow.to_dnn_input())[0][0] < 0.5
        self.premature_predictions.append(colored("{} => ({}) => {}".format(key, flow.flow_pkts_num, is_benign),
                      'green' if is_benign else 'red'))

    def close_flow(self, key):
        closed_flow_key = list(key)
        closed_flow_key.append(0)

        while tuple(closed_flow_key) in self.closed_flows:
            closed_flow_key[5] += 1

        self.closed_flows[tuple(closed_flow_key)] = self.flows[key]

        self.flows.pop(key)

    def get_ob(self, key):
        return self.flows[key] if key in self.flows else None

    def save(self, filepath):
        with open(filepath, "wb") as f:
            pickle.dump(self.flows, f)

    def load(self, filepath):
        with open(filepath, "rb") as f:
            self.flows = pickle.loads(f)

    def __del__(self):
        print("Closed")

    def __repr__(self):
        selfstr = ""
        for k, v in self.flows:
            selfstr += "{} => {}\n".format(k, repr(v))

        return selfstr
