import requests
import json


# Авторизация в HMS
def get_huawei_token(client_id, client_secret):
    url = "https://oauth-login.cloud.huawei.com/oauth2/v3/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, data=data)
    return response.json()["access_token"]


# Отправка данных на часы
def send_to_watch(data_dict):
    token = get_huawei_token("your_client_id", "your_client_secret")
    url = "https://healthapi.cloud.huawei.com/health/v1/data"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "dataCollections": [{
            "dataType": {
                "name": "custom.health.data_type"
            },
            "dataPoints": [{
                "startTime": int(time.time() * 1000),
                "endTime": int((time.time() + 60) * 1000),
                "fields": [{
                    "name": "value",
                    "format": "float",
                    "value": data_dict["value"]
                }]
            }]
        }]
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.status_code