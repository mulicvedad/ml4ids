import sys
print(sys.path)
# sys.path.append("/Users/vedad/Code/master/firewall_monitoring/source/ml/rootmodule/ml_models/base")
# sys.path.append("/Users/vedad/Code/master/firewall_monitoring/source/ml/rootmodule/ml_models")
# sys.path.append("/Users/vedad/Code/master/firewall_monitoring/source/ml/rootmodule/packet_sniffer")

import packet_sniffer.network_traffic_sniffer

# dir_with_csvs = "/Users/vedad/Code/master/firewall_monitoring/source/ml/" + dir_with_csvs
# if not os.path.exists(dir_with_csvs):