import random
import time
from typing import Any, Generator


def random_response() -> Generator[str, None, None]:
    response = random.choice([
        "The Amazon rainforest produces around 20% of the world’s oxygen; do you know that kind of massive ecosystem is still shrinking every year?",
        "Bananas are technically berries, but strawberries aren’t; do you know that kind of botanical twist comes from how the fruit develops?",
        "Your brain uses about 20% of your body’s energy; do you know that kind of demand is why thinking hard can actually feel tiring?"
    ])

    for word in response.split():
        yield word + " "
        time.sleep(0.05)