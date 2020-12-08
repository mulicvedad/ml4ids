from enum import IntEnum

from ml_for_ids.datasets.datset_info import IDSDataset


class FEATURE(IntEnum):
    FWD_PKTS_NUM = 0,
    BWD_PKTS_NUM = 1,
    FWD_PKT_LEN_MAX = 2,
    FWD_PKT_LEN_MIN = 3,
    FWD_PKT_LEN_MEAN = 4,
    FWD_PKT_LEN_STD = 5,
    BWD_PKT_LEN_MIN = 6,
    BWD_PKT_LEN_MEAN = 7,
    BWD_PKT_LEN_STD = 8,
    BYTES_PER_SEC = 9,
    PKTS_PER_SEC = 10,
    PKT_LEN_MIN = 11,
    PKT_LEN_MEAN = 12,
    PKT_LEN_STD = 13,
    PSH_FLAGS_NUM = 14,
    ACK_FLAGS_NUM = 15,
    FWD_SEGMENT_SIZE_MEAN = 16


SPECIFIC_FEATURES_TO_GENERIC_MAPPING = {
    IDSDataset.CSE_CIC_IDS_2017: {
        FEATURE.FWD_PKTS_NUM: " Total Fwd Packets",
        FEATURE.BWD_PKTS_NUM: " Total Backward Packets",
        FEATURE.FWD_PKT_LEN_MAX: " Fwd Packet Length Max",
        FEATURE.FWD_PKT_LEN_MIN: " Fwd Packet Length Min",
        FEATURE.FWD_PKT_LEN_MEAN: " Fwd Packet Length Mean",
        FEATURE.FWD_PKT_LEN_STD: " Fwd Packet Length Std",
        FEATURE.BWD_PKT_LEN_MIN: " Bwd Packet Length Min",
        FEATURE.BWD_PKT_LEN_MEAN: " Bwd Packet Length Mean",
        FEATURE.BWD_PKT_LEN_STD: " Bwd Packet Length Std",
        FEATURE.BYTES_PER_SEC: "Flow Bytes/s",
        FEATURE.PKTS_PER_SEC: " Flow Packets/s",
        FEATURE.PKT_LEN_MIN: " Min Packet Length",
        FEATURE.PKT_LEN_MEAN: " Packet Length Mean', ' Packet Length Std",
        FEATURE.PKT_LEN_STD: " PSH Flag Count",
        FEATURE.PSH_FLAGS_NUM: " ACK Flag Count",
        FEATURE.ACK_FLAGS_NUM: " Average Packet Size",
        FEATURE.FWD_SEGMENT_SIZE_MEAN: "Avg Fwd Segment Size"
    }
}
