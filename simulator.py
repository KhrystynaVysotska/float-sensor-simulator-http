import time
import json
import base64
import datetime
import requests

from configs.gcp_configs import *
from configs.http_configs import *
from configs.device_configs import *

from generators.jwt_generator import create_jwt
from generators.data_generator import generate_data


def publish_data(
        device_id,
        project_id,
        registry_id,
        cloud_region,
        algorithm,
        private_key_file,
        jwt_expires_minutes,
):
    jwt_iat = datetime.datetime.utcnow()
    jwt_exp_seconds = jwt_expires_minutes * 60
    jwt = create_jwt(project_id, private_key_file, algorithm, jwt_expires_minutes)

    headers = {'authorization': 'Bearer ' + jwt, 'content-type': 'application/json', 'cache-control': 'no-cache'}
    endpoint = "{}/projects/{}/locations/{}/registries/{}/devices/{}:publishEvent".format(
        HTTP_BASE_URL, project_id, cloud_region, registry_id, device_id
    )

    while True:
        seconds_since_issue = (datetime.datetime.utcnow() - jwt_iat).seconds
        if seconds_since_issue > jwt_exp_seconds:
            print("Refreshing token after {}s".format(seconds_since_issue))
            jwt_iat = datetime.datetime.utcnow()
            jwt = create_jwt(project_id, private_key_file, algorithm, jwt_expires_minutes)

        payload = base64.b64encode(generate_data(device_id).encode('utf-8'))
        data = {"binary_data": payload.decode("utf-8"), "sub_folder": TELEMETRY_TOPIC}
        response = requests.post(endpoint, headers=headers, json=data)

        print('Message published with status code: ' + str(response.status_code))

        time.sleep(PUBLISHING_FREQUENCY_IN_SECONDS)


if __name__ == '__main__':
    publish_data(
        jwt_expires_minutes=5,
        project_id=PROJECT_ID,
        cloud_region=REGION,
        registry_id=REGISTRY_ID,
        device_id=DEVICE_ID,
        algorithm="RS256",
        private_key_file=PRIVATE_KEY_FILE_PATH
    )
