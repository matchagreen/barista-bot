import os


def load_dotenv():
    with open('.env', 'r') as file:
        while True:
            line = file.readline()

            if not line:
                break

            k, v = line.strip().split('=')
            os.environ[k] = v
