#!/usr/bin/env bash

# This script is used for sampling of a large dataset.
# It randomly combines N rows from each CSV into a single output CSV.
# This way we have a representative CSV which can be processed faster.

# Root path for datasets. It can be specified via '-p' param. If not, this default value is used.
PATH="/Users/vedad/Code/master/firewall_monitoring/source/ml4ids/dataset"

while getopts ":p:d:o:" opt; do
  case $opt in
    p) PATH="$OPTARG"
    ;;
    d) DATASET="$OPTARG"
    ;;
    d) OUTPUT_DIR="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

if [[ $DATASET = "cicids17" ]]; then
    echo "its 17"
    PATH="${PATH}/cicids2017"
elif [[ $DATASET = "unsw" ]]; then
    echo "its unsw"
    PATH="${PATH}/unsw_nb15"
else
    echo "its 18"
    PATH="/Users/vedad/Other/etf/magistarski/datasets/cic-ids-2018"
fi


if [[ -e $DATASET ]]; then
    # defaulting to csecic18
    OUTPUT_DIR="/Users/vedad/Code/master/firewall_monitoring/source/ml4ids/dataset/csecic2018/predefined"
elif [[ -z "$OUTPUT_DIR" ]]; then
    echo "Emtpy output dir, will use default"
    OUTPUT_DIR="${PATH}/predefined"
fi

echo "Using data from path=$PATH"
echo "Using output dir=$OUTPUT_DIR"

TMP_CSV_PATH=${OUTPUT_DIR}/sample_data_prepare.csv
TMP_CLEAN_CSV_PATH=${OUTPUT_DIR}/sample_data_clean.csv
FINAL_CSV_PATH=${OUTPUT_DIR}/sample_data.csv

[[ ! -d $OUTPUT_DIR ]] && echo "Creating output dir" && /bin/mkdir -p $OUTPUT_DIR
[[ ! -e $TMP_CSV_PATH ]] && echo "Creating tmp csv" && /usr/bin/touch $TMP_CSV_PATH
[[ ! -e $TMP_CLEAN_CSV_PATH ]] && echo "Creating tmp clean csv" && /usr/bin/touch $TMP_CSV_PATH

# Extract random rows from each (CSV) file
for file in $PATH/data/*; do
    echo "Attempt to process the file=$file..."
    if [[ -f "$file" ]]; then
        echo "Processing file=$file..."
        # Randomly select N% lines
        /bin/cat ${file} | /usr/bin/awk 'BEGIN {srand()} !/^$/ { if (rand() <= .1) print $0}' >> ${TMP_CSV_PATH}
    fi
done

# Remove all rows with header values
/usr/bin/sed '/Protocol/d' ${TMP_CSV_PATH} >> ${TMP_CLEAN_CSV_PATH}


# Add headers as first row
echo -e "Dst Port,Protocol,Timestamp,Flow Duration,Tot Fwd Pkts,Tot Bwd Pkts,TotLen Fwd Pkts,TotLen Bwd Pkts,Fwd Pkt Len Max,Fwd Pkt Len Min,Fwd Pkt Len Mean,Fwd Pkt Len Std,Bwd Pkt Len Max,Bwd Pkt Len Min,Bwd Pkt Len Mean,Bwd Pkt Len Std,Flow Byts/s,Flow Pkts/s,Flow IAT Mean,Flow IAT Std,Flow IAT Max,Flow IAT Min,Fwd IAT Tot,Fwd IAT Mean,Fwd IAT Std,Fwd IAT Max,Fwd IAT Min,Bwd IAT Tot,Bwd IAT Mean,Bwd IAT Std,Bwd IAT Max,Bwd IAT Min,Fwd PSH Flags,Bwd PSH Flags,Fwd URG Flags,Bwd URG Flags,Fwd Header Len,Bwd Header Len,Fwd Pkts/s,Bwd Pkts/s,Pkt Len Min,Pkt Len Max,Pkt Len Mean,Pkt Len Std,Pkt Len Var,FIN Flag Cnt,SYN Flag Cnt,RST Flag Cnt,PSH Flag Cnt,ACK Flag Cnt,URG Flag Cnt,CWE Flag Count,ECE Flag Cnt,Down/Up Ratio,Pkt Size Avg,Fwd Seg Size Avg,Bwd Seg Size Avg,Fwd Byts/b Avg,Fwd Pkts/b Avg,Fwd Blk Rate Avg,Bwd Byts/b Avg,Bwd Pkts/b Avg,Bwd Blk Rate Avg,Subflow Fwd Pkts,Subflow Fwd Byts,Subflow Bwd Pkts,Subflow Bwd Byts,Init Fwd Win Byts,Init Bwd Win Byts,Fwd Act Data Pkts,Fwd Seg Size Min,Active Mean,Active Std,Active Max,Active Min,Idle Mean,Idle Std,Idle Max,Idle Min,Label\n$(/bin/cat ${TMP_CLEAN_CSV_PATH})" > ${FINAL_CSV_PATH}


/bin/rm ${TMP_CSV_PATH} ${TMP_CLEAN_CSV_PATH}
