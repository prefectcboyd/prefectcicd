from prefect import task, flow, get_run_logger
import time

def this_is_not_a_task(logger):
    logger.info("I am not a task context")


@task()
def log_platform_info():
    logger = get_run_logger()
    logger.info("hello world")
    this_is_not_a_task(logger)


@flow(log_prints=True)
def hello_world():
    logger = get_run_logger()
    log_platform_info()
    time.sleep(300)


if __name__ == "__main__":
    hello_world()
    time.sleep(300)
    print("test")