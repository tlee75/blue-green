import json
import logging
import os
import requests
import time
from typing import Dict

# Configure logger to write to file
logging.basicConfig(filename='myapp.log',
                    filemode='w',
                    level=logging.INFO,
                    format='%(asctime)s: %(levelname)s - %(message)s')

# Create logger object and set level
logger: logging.getLogger = logging.getLogger("http-client")
logger.setLevel(logging.DEBUG)

# Prep
server_url: str = os.getenv("SERVER_URL", 'http://localhost')
server_port: str = os.getenv("PORT", '8080')
req_timeout: int = 3
code_summary: Dict = {}
app_versions: set = set()
num_polling_events: int = 100
request_delay: int = 0

def display_summary():
    """
    Display HTTP code counts and detected versions
    """
    for key,value in code_summary.items():
        logger.info(f"HTTP {key}'s: {value}")
    logger.info(f"Versions encountered: {app_versions}")


def process_resp(code, content):
    """
    Build a summary of HTTP code counts and app versions
    """
    # Avoid empty dict errors
    code_summary[code]: int = code_summary.get(code, 0) + 1

    # Store and emit version number
    try:
        version_number: str = json.loads(content).get("version")
        app_versions.add(version_number)
        logger.info(version_number)
    except json.JSONDecodeError:
        logger.error("JSON Decoding exception")


def get_version():
    """
    Make the HTTP request
    """
    try:
        resp = requests.get(f'{server_url}:{server_port}/version', timeout=req_timeout)
        process_resp(code=resp.status_code, content=resp.content)
    except requests.exceptions.ConnectionError as conn_err:
        logger.error("Connection error", conn_err)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)


def main():
    """
    Fetch the version from the endpoint until we detect the switch
    """

    logger.info('Started')
    print("Script will continuously log to file until the version switch is detected...")

    while True:
        start_time: time.time = time.time()
        for _ in range(num_polling_events):
            get_version()
            time.sleep(request_delay)
        elapsed_time: time.time = time.time() - start_time
        request_rate: float = num_polling_events / elapsed_time
        logger.info(f"Requests Rate: {request_rate:.2f}/s")

        # Check if we can break out of loop
        if len(app_versions) > 1:
            logger.info("Detected multiple versions, traffic has shifted")
            break

    display_summary()
    logger.info("Stopped")


if __name__ == "__main__":
    main()
