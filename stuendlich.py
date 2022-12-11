import datetime
import json
from dataclasses import dataclass
from pathlib import Path
from urllib import request
from zoneinfo import ZoneInfo


@dataclass
class Config:
    access_token: str
    timezone: str
    template: str
    server_url: str
    visibility: str


def load_config(fn):
    data = json.load(fn.open())
    return Config(**data)


def send_message(config):
    dt = datetime.datetime.now(ZoneInfo(config.timezone))
    data = {
        "status": config.template.format(time=dt.strftime("%H:%M")),
        "visibility": config.visibility,
    }

    data = json.dumps(data).encode("utf-8")
    url = f"https://{config.server_url}/api/v1/statuses"
    headers = {
        "Authorization": f"Bearer {config.access_token}",
        "Content-Type": "application/json",
    }
    response = request.urlopen(request.Request(url, data=data, headers=headers))
    if response.status != 200:
        print(json.loads(response.read().decode("utf-8")))


def main():
    config = load_config((Path(__file__).parent.absolute() / "config.json"))
    send_message(config)


if __name__ == "__main__":
    main()
