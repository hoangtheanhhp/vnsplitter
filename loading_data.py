from io import open
import os.path

def load_data_train(path):
    f = open(path, encoding="UTF-8")
    file = ''.join(f.readlines())
    f.close()
    return file

if __name__ == "__main__":
    print load_data_train()

