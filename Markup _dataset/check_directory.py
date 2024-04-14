import os

class_dir = {0: "nothing", 1: "account", 2:"card", 3:"passport", 4:"phone", 5:"snils", 6:"qr"}

def check_dir():
    for data_id in class_dir:
        print(class_dir[data_id])
        if not os.path.exists(f"data/{class_dir[data_id]}"):
            os.makedirs(f"data/{class_dir[data_id]}")


check_dir()