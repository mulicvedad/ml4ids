import sys
sys.path.append('/Users/vedad/Code/master/firewall_monitoring/source/ml')

from os import getuid
from glob import glob
from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import TCP, UDP
from termcolor import colored
from argparse import ArgumentParser

from ml_for_ids.datasets.datset_info import IDSDataset
from ml_for_ids.ml_models.dnn import SimpleDNNModel
from packet_sniffer.observations_dict import FlowCollection

PROTO_TCP = 6
PROTO_UDP = 17

PCAPS = glob(os.path.join("/Users/vedad/Downloads/PCAP-03-11/", "*"))
# [
#     "/Users/vedad/Code/master/firewall_monitoring/source/ml/pcaps/SAT-01-12-2018_0818.pcap"
# "/Users/vedad/Code/master/firewall_monitoring/source/ml/pcaps/can-2003-0003.pcap",
# "/Users/vedad/Code/master/firewall_monitoring/source/ml/pcaps/can-2003-0003 (1).pcap",
# "/Users/vedad/Code/master/firewall_monitoring/source/ml/pcaps/dns-remoteshell.pcap",
# "/Users/vedad/Code/master/firewall_monitoring/source/ml/pcaps/egypt-packetlogic-ttl-localization.pcap",
# "/Users/vedad/Code/master/firewall_monitoring/source/ml/pcaps/EXPLOIT_metasploit-cve-2012-1723_EmergingThreats.pcap",
# "/Users/vedad/Code/master/firewall_monitoring/source/ml/pcaps/EXPLOIT_metasploit-f5-CVE-2012-1493_EmergingThreats.pcap",
# "/Users/vedad/Code/master/firewall_monitoring/source/ml/pcaps/EXPLOIT_metasploit-ie-sameid-CVE-2012-1875_EmergingThreats.pcap",
# "/Users/vedad/Code/master/firewall_monitoring/source/ml/pcaps/EXPLOIT_metasploit-itunes-m3u-CVE-2012-0677_EmergingThreats.pcap",
# "/Users/vedad/Code/master/firewall_monitoring/source/ml/pcaps/EXPLOIT_metasploit_ie_aurora_exploitWin2k3_EvilFingers.pcap",
# "/Users/vedad/Code/master/firewall_monitoring/source/ml/pcaps/EXPLOIT_metasploit_ie_aurora_WinXP_successfulExploitation_EvilFingers.pcap",
# "/Users/vedad/Code/master/firewall_monitoring/source/ml/pcaps/http-flood.pcap",
# "/Users/vedad/Code/master/firewall_monitoring/source/ml/pcaps/turkey-malware-injection.pcap",
# "/Users/vedad/Code/master/firewall_monitoring/source/ml/pcaps/zlip-1.pcap",
# "/Users/vedad/Code/master/firewall_monitoring/source/ml/pcaps/zlip-2.pcap",
# "/Users/vedad/Code/master/firewall_monitoring/source/ml/pcaps/zlip-3.pcap"
# ]

SUPPORTED_PROTOCOLS = [PROTO_TCP, PROTO_UDP]

model = SimpleDNNModel(dataset_dir_name=IDSDataset.CSE_CIC_IDS_2017.get_dataset_dir())
model.load()
main_flow_collection = FlowCollection(model)

def parse_cmd_args():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-o", "--offline", action="store_true", help="Save training output")
    return arg_parser.parse_args()

def process_packet(pkt):
    try:
        if pkt.haslayer(IP) and (pkt[IP].proto in SUPPORTED_PROTOCOLS) and (pkt.haslayer(UDP) or pkt.haslayer(TCP)):
            proto = UDP if pkt[IP].proto == 17 else TCP
            protoStr = 'TCP' if pkt[IP].proto == PROTO_TCP else 'UDP'
            ip_src=pkt[IP].src
            ip_dst=pkt[IP].dst
            tcp_src = pkt[proto].sport
            tcp_dst = pkt[proto].dport
            main_flow_collection.add_packet(protoStr, ip_src, tcp_src, ip_dst, tcp_dst, pkt)
            if len(main_flow_collection.premature_predictions) > 100 and len(main_flow_collection.premature_predictions) < 110:
                for x in main_flow_collection.premature_predictions:
                    print(x)
    except:
        print("Exception")
        sys.exc_info()


def show_stats():
    print(repr(main_flow_collection))


def main():
    args = parse_cmd_args()

    if getuid() == 0 or args.offline:
        try:
            if args.offline:
                sniff_from_pcaps(PCAPS)
                quit(0)
            else:
                sniff(filter="ip and (host 157.240.9.35 or 157.240.9.174 or 172.217.18.78 or 104.22.11.161 or 172.67.10.190 or 104.22.10.16 or 94.23.249.32 or 23.57.192.93)",
                      count=10000, prn=process_packet)
            predict(main_flow_collection.flows.items())
            print("============== CLOSED FLOWS ===============")
            predict(main_flow_collection.closed_flows.items())
        except KeyboardInterrupt:
            print("Keyboard interrupt after packets")
            quit(1)
        except:
            sys.exc_info()
            quit(1)
        finally:
            quit(0)
    else:
        print("Must run as root")
        quit()


def sniff_from_pcaps(pcaps):
    for pcap in pcaps:
        try:
            sniff(count=100000, prn=process_packet, offline=pcap)
            predict(main_flow_collection.flows.items())
            print("============== CLOSED FLOWS ===============")
            predict(main_flow_collection.closed_flows.items())
        except:
            print(colored("Failed for {}".format(pcap)))


def predict(flows):
    num_attack_flows = 0
    num_all_flows = len(flows)
    for k, flow in flows:
        if flow.flow_pkts_num < 10:
            num_all_flows -= 1
            continue
        flow.snapshot()
        is_benign = model.predict(flow.to_dnn_input())[0][0] < 0.5
        if is_benign == False:
            num_attack_flows += 1
        print_prediction(k, flow, is_benign)
    print("Percent of attack flows: {} %".format((num_attack_flows * 1. / num_all_flows) * 100))


def print_prediction(flow_key, flow, is_benign):
    print(colored("{} => ({}) => {}".format(flow_key, flow.flow_pkts_num, is_benign), 'green' if is_benign else 'red'))


main()
