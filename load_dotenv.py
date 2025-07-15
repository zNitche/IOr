import os


def load_dotenv(file_path: str):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()

            for line in lines:
                split_line = line.split("=")
                
                if len(split_line) == 2:
                    name, value = split_line
                    os.environ[name] = value.rstrip()

    else:
        print(f"{file_path} doesn't exist, skipping...")
