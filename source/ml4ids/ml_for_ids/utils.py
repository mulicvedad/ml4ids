import glob
import os
import datetime


def get_time_based_file_name(extension):
    now = datetime.datetime.now()
    return now.strftime("%Y_%m_%d_%H_%M_%S") + "." + extension


def get_time_based_dir_name():
    now = datetime.datetime.now()
    return now.strftime("%Y_%m_%d_%H_%M_%S")


def save_json_to_file(output_dir, json):
    if not os.path.exists(output_dir):
        raise Exception("Specified directory not found, dir={}".format(output_dir))

    final_path = os.path.join(output_dir, get_time_based_file_name("json"))

    with open(final_path, "w+") as json_file:
        json_file.write(json)

    return final_path


def load_last_file(dir, extension="json"):
    if not os.path.exists(dir):
        dir = '/Users/vedad/Code/master/firewall_monitoring/source/ml/ml_for_ids/' + dir
        if not os.path.exists(dir):
            raise Exception("Specified directory not found")

    list_of_jsons = glob.glob("{}/*.{}".format(dir, extension))
    latest_file = max(list_of_jsons, key=os.path.getctime)

    return latest_file, open(latest_file, "r").read()

