from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
import numpy as np

from scapy.layers.inet import IP, TCP, UDP, NoPayload

import sys
sys.path.append("/Users/vedad/Code/master/firewall_monitoring/source/ml/rootmodule/packet_sniffer/statistics_util")
from packet_sniffer.statistics_util.statistics_utils import update_mean_std, update_avg

class FlowEntry:
    def __init__(self):
        # Direction agnostic features
        self.flow_pkts_num = 0
        self.all_bytes_num = 0
        self.bytes_per_sec = None
        self.pkts_per_sec = None

        # Packet size - global
        self.pkt_len_min = None
        self.pkt_len_max = None
        self.pkt_len_mean = None
        self.pkt_len_std = None

        # Flags
        self.ack_flags_num = 0
        self.psh_flags_num = 0

        # Number of packets in each direction
        self.fwd_pkts_num = 0
        self.bwd_pkts_num = 0

        # Packet size - fwd
        self.fwd_pkt_len_min = None
        self.fwd_pkt_len_max = None
        self.fwd_pkt_len_mean = None
        self.fwd_pkt_len_std = None

        # Packet size - bwd
        self.bwd_pkt_len_min = None
        self.bwd_pkt_len_max = None
        self.bwd_pkt_len_mean = None
        self.bwd_pkt_len_std = None

        # Segment size - fwd
        self.fwd_segment_size_min = None
        self.fwd_segment_size_max = None
        self.fwd_segment_size_mean = None
        self.fwd_segment_size_std = None

        # Segment size - bwd
        self.bwd_segment_size_min = None
        self.bwd_segment_size_max = None
        self.bwd_segment_size_mean = None
        self.bwd_segment_size_std = None

        # Meta
        self.started = datetime.now()
        self.timeout = False  # done
        self.closed = False  # done

    def __repr__(self):
        return "{}, {}".format(self.fwd_pkts_num, self.bwd_pkts_num)

    def add_direction_agnostic_features(self, pkt):
        self.flow_pkts_num += 1
        ip_pkt_len = pkt[IP].len
        self.all_bytes_num += ip_pkt_len

        # pkt len
        if not self.pkt_len_min or ip_pkt_len < self.pkt_len_min:
            self.pkt_len_min = ip_pkt_len

        if not self.pkt_len_max or ip_pkt_len > self.pkt_len_max:
            self.pkt_len_max = ip_pkt_len

        (self.pkt_len_mean, self.pkt_len_std) = update_mean_std(self.pkt_len_mean or ip_pkt_len, self.pkt_len_std or 0,
                                                                self.flow_pkts_num, ip_pkt_len)

        if 'A' in pkt.flags:
            self.ack_flags_num += 1

        if 'P' in pkt.flags:
            self.psh_flags_num += 1

        if 'F' in pkt.flags:
            self.closed = True

    def add_fwd(self, pkt):
        self.add_direction_agnostic_features(pkt)
        self.fwd_pkts_num += 1
        ip_pkt_len = pkt[IP].len

        if not self.fwd_pkt_len_min or ip_pkt_len < self.fwd_pkt_len_min:
            self.fwd_pkt_len_min = ip_pkt_len

        if not self.fwd_pkt_len_max or ip_pkt_len > self.fwd_pkt_len_max:
            self.fwd_pkt_len_max = ip_pkt_len

        (self.fwd_pkt_len_mean, self.fwd_pkt_len_std) = update_mean_std(self.fwd_pkt_len_mean or ip_pkt_len,
                                                                        self.fwd_pkt_len_std or 0,
                                                                        self.fwd_pkts_num,
                                                                        ip_pkt_len)

        self.check_timed_out(60)

        if TCP in pkt and not isinstance(pkt[TCP].payload, NoPayload):
            tcp_seg_len = len(pkt[TCP].payload)
            self.fwd_segment_size_mean = update_avg(self.fwd_segment_size_mean or 0, self.fwd_pkts_num, tcp_seg_len)
        elif UDP in pkt and not isinstance(pkt[UDP].payload, NoPayload):
            udp_segment_len = len(pkt[UDP].payload)
            self.fwd_segment_size_mean = update_avg(self.fwd_segment_size_mean or 0, self.fwd_pkts_num, udp_segment_len)

    def add_bwd(self, pkt):
        self.add_direction_agnostic_features(pkt)
        self.bwd_pkts_num += 1
        ip_pkt_len = pkt[IP].len

        if not self.bwd_pkt_len_min or ip_pkt_len < self.bwd_pkt_len_min:
            self.bwd_pkt_len_min = ip_pkt_len

        if not self.bwd_pkt_len_max or ip_pkt_len > self.bwd_pkt_len_max:
            self.bwd_pkt_len_max = ip_pkt_len

        (self.bwd_pkt_len_mean, self.bwd_pkt_len_std) = update_mean_std(self.bwd_pkt_len_mean or ip_pkt_len,
                                                                        self.bwd_pkt_len_std or 0,
                                                                        self.bwd_pkts_num,
                                                                        ip_pkt_len)

        if TCP in pkt and not isinstance(pkt[TCP].payload, NoPayload):
            tcp_segment_len = len(pkt[TCP].payload)
            self.bwd_segment_size_mean = update_avg(self.bwd_segment_size_mean or 0, self.bwd_pkts_num, tcp_segment_len)
        elif UDP in pkt and not isinstance(pkt[UDP].payload, NoPayload):
            udp_segment_len = len(pkt[UDP].payload)
            self.bwd_segment_size_mean = update_avg(self.bwd_segment_size_mean or 0, self.bwd_pkts_num, udp_segment_len)

        self.check_timed_out(60)

    def check_timed_out(self, timeout_s):
        if (datetime.now() - self.started).total_seconds() >= timeout_s:
            self.timeout = True
            self.snapshot()

    def snapshot(self):
        flow_duration_sec = (datetime.now() - self.started).total_seconds()
        if flow_duration_sec >= 1:
            self.bytes_per_sec = self.all_bytes_num / (flow_duration_sec + 1)
            self.pkts_per_sec = self.flow_pkts_num / (flow_duration_sec + 1)
        else:
            self.bytes_per_sec = self.all_bytes_num
            self.pkts_per_sec = self.flow_pkts_num

    def to_dnn_input(self):
        arr =  np.array([self.fwd_pkts_num, self.bwd_pkts_num, self.fwd_pkt_len_max, self.fwd_pkt_len_min, self.fwd_pkt_len_mean,
                self.fwd_pkt_len_std, self.bwd_pkt_len_min, self.bwd_pkt_len_mean, self.bwd_pkt_len_std, self.bytes_per_sec,
                self.pkts_per_sec,
                self.pkt_len_min, self.pkt_len_mean, self.pkt_len_std, self.psh_flags_num, self.ack_flags_num,
                #  ''' Down/Up Ratio''',
                self.pkt_len_mean, self.fwd_segment_size_mean, self.bwd_segment_size_mean]).astype(float)
        # '''Subflow Fwd Packets', 'Subflow Bwd Packets', 'act_data_pkt_fwd'''
        max_vals = np.array([219759, 291922, 24820, 2325, 5940.86, 7125.6, 2896, 5800.5, 8194.66, 100, 10, 1448, 3337.14, 4731.52, 1, 1, 3893.33, 5940.86, 5800.5])
        return (arr / max_vals).reshape(1, 19)



#  Total Fwd Packets                   219759
#  Total Backward Packets              291922
#  Fwd Packet Length Max                24820
#  Fwd Packet Length Min                 2325
#  Fwd Packet Length Mean             5940.86
#  Fwd Packet Length Std               7125.6
#  Bwd Packet Length Min                 2896
#  Bwd Packet Length Mean              5800.5
#  Bwd Packet Length Std              8194.66
#  Min Packet Length                     1448
#  Packet Length Mean                 3337.14
#  Packet Length Std                  4731.52
#  PSH Flag Count                           1
#  ACK Flag Count                           1
#  Average Packet Size                3893.33
#  Avg Fwd Segment Size               5940.86
#  Avg Bwd Segment Size                5800.5