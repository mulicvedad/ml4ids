from enum import IntEnum

DATASET_ROOT_DIR = "dataset/"
DATASET_DIRS = [
    "unsw_nb15/data",
    "cicids2017/data",
    "cicids2018/data"
]
ALL_FEATURES = [
    ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss', 'sinpkt', 'dinpkt',
     'sjit', 'djit', 'swin', 'stcpb', 'dtcpb', 'dwin', 'tcprtt', 'synack', 'ackdat', 'smean', 'dmean', 'trans_depth',
     'response_body_len', 'ct_srv_src', 'ct_state_ttl', 'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm',
     'ct_src_ltm', 'ct_srv_dst', 'label'],

    # '''Down/Up Ratio''' '''Subflow Fwd Packets''' '''Subflow Bwd Packets''' '''act_data_pkt_fwd'''
    [' Total Fwd Packets', ' Total Backward Packets', ' Fwd Packet Length Max', ' Fwd Packet Length Min', ' Fwd Packet Length Mean',' Fwd Packet Length Std', ' Bwd Packet Length Min', ' Bwd Packet Length Mean', ' Bwd Packet Length Std', ' Min Packet Length', ' Packet Length Mean', ' Packet Length Std', ' PSH Flag Count', ' ACK Flag Count', ' Average Packet Size',' Avg Fwd Segment Size', ' Avg Bwd Segment Size', ' Label'],

    ['''Protocol',''' 'Tot Fwd Pkts', 'Tot Bwd Pkts', 'Fwd Pkt Len Max', 'Fwd Pkt Len Min', 'Fwd Pkt Len Mean', 'Fwd Pkt Len Std',
     'Bwd Pkt Len Max', 'Bwd Pkt Len Min', 'Bwd Pkt Len Mean', 'Bwd Pkt Len Std', 'Flow Byts/s', 'Flow Pkts/s', 'Pkt Len Min',
     'Pkt Len Max', 'Pkt Len Mean', 'Pkt Len Std', 'RST Flag Cnt', 'PSH Flag Cnt', 'ACK Flag Cnt', 'ECE Flag Cnt', 'Down/Up Ratio',
     'Pkt Size Avg', 'Fwd Seg Size Avg', 'Bwd Seg Size Avg', 'Subflow Fwd Pkts', 'Subflow Bwd Pkts', 'Fwd Act Data Pkts',
     'Fwd Seg Size Min', 'Label']
]


class IDSDataset(IntEnum):
    UNSW_NB15 = 1
    CSE_CIC_IDS_2017 = 2
    CSE_CIC_IDS_2018 = 3

    def get_dataset_dir(self):
        return DATASET_DIRS[self.value - 1]

    def get_attrs(self):
        return ALL_FEATURES[self.value - 1]

    @staticmethod
    def get_target_map_fun(dataset):
        if dataset == IDSDataset.UNSW_NB15:
            return None
        else:
            return lambda x: 0 if str(x).lower() == "benign" else 1