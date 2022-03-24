import os


def list_files():
    listing = os.listdir(os.getcwd())
    for file in listing:
        print(file)
