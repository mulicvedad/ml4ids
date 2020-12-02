from packet_sniffer import update_mean_std, update_avg

test_list = [1, 3, 5, 1, 2.4, 3.5, 6.2, 3.4]

mean = None
std = None
avg = None
num = 0

for x in test_list:
    num += 1
    mean, std = update_mean_std(mean or x, std or 0, num, x)
    avg = update_avg(avg or 0, num, x)
    print("==> Mean: {} \t\t Std: {} \t\t Avg: {}".format(mean, std, avg))

print("[FINAL] Mean: {} \t\t Std: {} \t\t Avg: {}".format(mean, std, avg))
