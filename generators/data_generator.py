import json
import random
import datetime


def generate_data(device_id):
    river_water_level = random.random()

    data = {"id": device_id, "timestamp": str(datetime.datetime.utcnow()), "river_water_level": river_water_level}

    return json.dumps(data)
