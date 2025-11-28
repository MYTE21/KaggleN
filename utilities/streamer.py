import re
import time


def response_generator(message: str):
    tokens = re.split(r"(\s+)", message)

    for token in tokens:
        yield token
        time.sleep(0.02)