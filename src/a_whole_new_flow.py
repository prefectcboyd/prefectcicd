import requests
import json
from prefect import flow, get_run_logger


@flow
def get_random_pun():
    logger = get_run_logger()
    url = "https://icanhazdadjoke.com/"
    headers = {
        "Accept": "application/json"
    }
    
    try:
        logger.info("Getting random pun")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        
        joke_data = response.json()
        logger.info(f"{joke_data.get('joke', 'No joke found')}")
        return joke_data.get("joke", "No joke found")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error: {e}")
        return f"Error: {e}"


if __name__ == "__main__":
    TIER = environ.get('WORK_POOL', 'dev')
    flow.from_source(
        "https://github.com/prefectcboyd/prefectcicd.git",
        entrypoint="src/a_whole_new_flow:get_random_pun",
    ).deploy(
        name=f"a_whole_new_flow_{TIER}",
        work_pool_name=f"{TIER}",
        build=False
    )
