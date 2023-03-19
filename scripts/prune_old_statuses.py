import datetime
import os

import requests

BASE_URL = "https://fedi.cress.space"
PRUNE_OLDER_THAN_DAYS = 28
# add gotosocial access token to repo secrets in Github
TOKEN = os.environ["GOTOSOCIAL_ACCESS_TOKEN"]
headers = {"Authorization": f"Bearer {TOKEN}"}

# get account_id of logged in user
r = requests.get(
    url=f"{BASE_URL}/api/v1/accounts/verify_credentials",
    headers=headers,
)
account_id = r.json()["id"]

max_id = None  # for pagination
while True:
    r = requests.get(
        url=f"{BASE_URL}/api/v1/accounts/{account_id}/statuses",
        headers=headers,
        params={"max_id": max_id},
    )

    result = r.json()
    if not len(result):
        break

    for item in result:
        dt = datetime.datetime.strptime(item.get("created_at"), "%Y-%m-%dT%H:%M:%S.%fZ")
        status_id = item.get("id")
        delete = bool(
            dt
            < (datetime.datetime.now() - datetime.timedelta(days=PRUNE_OLDER_THAN_DAYS))
        )
        print(status_id, delete, dt, item.get("content"))
        max_id = item.get("id")
        if delete:
            r = requests.delete(
                url=f"{BASE_URL}/api/v1/statuses/{status_id}",
                headers=headers,
            )
            if r.status_code == 200:
                print("deleted", status_id)
            else:
                print(r)
