import os

if __name__ == "__main__":
    directory_contents = os.listdir()
    print(directory_contents)

    if "data" not in directory_contents:
        os.mkdir("data")
