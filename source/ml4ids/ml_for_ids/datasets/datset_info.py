from enum import Enum, IntEnum


class IDSDataset(IntEnum):
    UNSW_NB15 = 1
    CSE_CIC_IDS_2017 = 2
    CSE_CIC_IDS_2018 = 3

    def get_dataset_dir(self):
        return DATASET_DIRS[self.value - 1]

    def get_sample_csv_path(self):
        return SAMPLE_CSVS[self.value - 1]

    def get_attrs(self):
        return ALL_FEATURES[self.value - 1]

    def get_cols_to_ignore(self):
        if self == IDSDataset.CSE_CIC_IDS_2018:
            return CICIDS18Feature.get_cols_to_ignore()
        else:
            return []

    @staticmethod
    def get_target_map_fun(dataset):
        if dataset == IDSDataset.UNSW_NB15:
            return None
        else:
            return lambda x: 0 if str(x).lower() == "benign" else 1


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
    [' Total Fwd Packets', ' Total Backward Packets', ' Fwd Packet Length Max', ' Fwd Packet Length Min', ' Fwd Packet Length Mean',
     ' Fwd Packet Length Std', ' Bwd Packet Length Min', ' Bwd Packet Length Mean', ' Bwd Packet Length Std', ' Min Packet Length',
     ' Packet Length Mean', ' Packet Length Std', ' PSH Flag Count', ' ACK Flag Count', ' Average Packet Size',' Avg Fwd Segment Size',
     ' Avg Bwd Segment Size', ' Label'],


    ['''Protocol',''' 'Tot Fwd Pkts', 'Tot Bwd Pkts', 'Fwd Pkt Len Max', 'Fwd Pkt Len Min', 'Fwd Pkt Len Mean', 'Fwd Pkt Len Std',
     'Bwd Pkt Len Max', 'Bwd Pkt Len Min', 'Bwd Pkt Len Mean', 'Bwd Pkt Len Std', 'Flow Byts/s', 'Flow Pkts/s', 'Pkt Len Min',
     'Pkt Len Max', 'Pkt Len Mean', 'Pkt Len Std', 'RST Flag Cnt', 'PSH Flag Cnt', 'ACK Flag Cnt', 'ECE Flag Cnt', 'Down/Up Ratio',
     'Pkt Size Avg', 'Fwd Seg Size Avg', 'Bwd Seg Size Avg', 'Subflow Fwd Pkts', 'Subflow Bwd Pkts', 'Fwd Act Data Pkts',
     'Fwd Seg Size Min', 'Label']
]
SAMPLE_CSVS = [
    DATASET_ROOT_DIR + "unsw_nb15/predefined/sample_data.csv",
    DATASET_ROOT_DIR + "cicids2017/predefined/sample_data.csv",
    DATASET_ROOT_DIR + "cicids2018/predefined/sample_data.csv"
]


# Features with their column names from dataset, i.g. the left is enum and the righ is column name
class CICIDS18Feature(Enum):
    FL_DUR = "Flow Duration"
    TOT_FW_PK = "Tot Fwd Pkts"
    TOT_BW_PK = "Tot Bwd Pkts"
    TOT_L_FW_PKT = "TotLen Fwd Pkts"
    TOT_L_BW_PKT = "TotLen Bwd Pkts"
    FW_PKT_L_MAX = "Fwd Pkt Len Max"
    FW_PKT_L_MIN = "Fwd Pkt Len Min"
    FW_PKT_L_AVG = "Fwd Pkt Len Mean"
    FW_PKT_L_STD = "Fwd Pkt Len Std"
    BW_PKT_L_MAX = "Bwd Pkt Len Max"
    BW_PKT_L_MIN = "Bwd Pkt Len Min"
    BW_PKT_L_AVG = "Bwd Pkt Len Mean"
    BW_PKT_L_STD = "Bwd Pkt Len Std"
    FL_BYT_S = "Flow Byts/s"
    FL_PKT_S = "Flow Pkts/s"
    FL_IAT_AVG = "Flow IAT Mean"
    FL_IAT_STD = "Flow IAT Std"
    FL_IAT_MAX = "Flow IAT Max"
    FL_IAT_MIN = "Flow IAT Min"
    FW_IAT_TOT = "Fwd IAT Tot"
    FW_IAT_AVG = "Fwd IAT Mean"
    FW_IAT_STD = "Fwd IAT Std"
    FW_IAT_MAX = "Fwd IAT Max"
    FW_IAT_MIN = "Fwd IAT Min"
    BW_IAT_TOT = "Bwd IAT Tot"
    BW_IAT_AVG = "Bwd IAT Mean"
    BW_IAT_STD = "Bwd IAT Std"
    BW_IAT_MAX = "Bwd IAT Max"
    BW_IAT_MIN = "Bwd IAT Min"
    FW_PSH_FLAG = "Fwd PSH Flags"
    BW_PSH_FLAG = "Bwd PSH Flags"
    FW_URG_FLAG = "Fwd URG Flags"
    BW_URG_FLAG = "Bwd URG Flags"
    FW_HDR_LEN = "Fwd Header Len"
    BW_HDR_LEN = "Bwd Header Len"
    FW_PKT_S = "Fwd Pkts/s"
    BW_PKT_S = "Bwd Pkts/s"
    PKT_LEN_MIN = "Pkt Len Min"
    PKT_LEN_MAX = "Pkt Len Max"
    PKT_LEN_AVG = "Pkt Len Mean"
    PKT_LEN_STD = "Pkt Len Std"
    PKT_LEN_VA = "Pkt Len Var"
    FIN_CNT = "FIN Flag Cnt"
    SYN_CNT = "SYN Flag Cnt"
    RST_CNT = "RST Flag Cnt"
    PST_CNT = "PSH Flag Cnt"
    ACK_CNT = "ACK Flag Cnt"
    URG_CNT = "URG Flag Cnt"
    CWE_CNT = "CWE Flag Count"
    ECE_CNT = "ECE Flag Cnt"
    DOWN_UP_RATIO = "Down/Up Ratio"
    PKT_SIZE_AVG = "Pkt Size Avg"
    FW_SEG_AVG = "Fwd Seg Size Avg"
    BW_SEG_AVG = "Bwd Seg Size Avg"
    FW_BYT_BLK_AVG = "Fwd Byts/b Avg"
    FW_PKT_BLK_AVG = "Fwd Pkts/b Avg"
    FW_BLK_RATE_AVG = "Fwd Blk Rate"
    BW_BYT_BLK_AVG = "Bwd Byts/b Avg"
    BW_PKT_BLK_AVG = "Bwd Pkts/b Avg"
    BW_BLK_RATE_AVG = "Bwd Blk Rate"
    SUBFL_FW_PK = "Subflow Fwd Pkts"
    SUBFL_FW_BYT = "Subflow Fwd Byts"
    SUBFL_BW_PKT = "Subflow Bwd Pkts"
    SUBFL_BW_BYT = "Subflow Bwd Byts"
    FW_WIN_BYT = "Init Fwd Win Byts"
    BW_WIN_BYT = "Init Bwd Win Byts"
    FW_ACT_PKT = "Fwd Act Data Pkts"
    FW_SEG_MIN = "Fwd Seg Size Min"
    ATV_AVG = "Active Mean"
    ATV_STD = "Active Std"
    ATV_MAX = "Active Max"
    ATV_MIN = "Active Min"
    IDL_AVG = "Idle Mean"
    IDL_STD = "Idle Std"
    IDL_MAX = "Idle Max"
    IDL_MIN = "Idle Min"
    LABEL = "Label"

    # Ignored
    DST_PORT = "Dst Port"
    PROTOCOL = "Protocol"
    TIMESTAMP = "Timestamp"

    def get_raw_col_name(self):
        return self.value

    @staticmethod
    def get_label_col_name():
        return CICIDS18Feature.LABEL.value

    @staticmethod
    def get_cols_to_ignore():
        return [
            # Discarded empirically
            CICIDS18Feature.DST_PORT.value,
            CICIDS18Feature.TIMESTAMP.value,
            CICIDS18Feature.PROTOCOL.value,

            # Discarded because of low score in sklearn::SelectKBest (using chi2 and f_classif as scoring functions)
            CICIDS18Feature.DOWN_UP_RATIO.value,
            CICIDS18Feature.PST_CNT.value,
            CICIDS18Feature.BW_HDR_LEN.value,
            CICIDS18Feature.FW_HDR_LEN.value,
            CICIDS18Feature.BW_PKT_L_STD.value,
            CICIDS18Feature.TOT_BW_PK.value,
            CICIDS18Feature.SUBFL_BW_PKT.value,
            CICIDS18Feature.TOT_FW_PK.value,
            CICIDS18Feature.SUBFL_FW_PK.value,
            CICIDS18Feature.FW_ACT_PKT.value,
            CICIDS18Feature.BW_PKT_L_MAX.value,
            CICIDS18Feature.TOT_L_BW_PKT.value,
            CICIDS18Feature.SUBFL_BW_BYT.value
        ]
