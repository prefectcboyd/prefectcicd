"""Deployment script for Prefect2 (Kubernetes Job block + Prefect Deployment)."""
import sys
from os import environ, path
from prefect.deployments import Deployment
from main_flow import hello_world
from prefect.filesystems import GitHub

# sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), "../src")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Verify Environment Variables
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("Verifying environment variables...")
print(environ.get("WORK_POOL"))
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

# retrieve dynamic variables from environment
TIER_ENVIRONMENT = environ.get("WORK_POOL", "dev").upper()
WORK_POOL = environ.get("WORK_POOL", "dev")
GCP_PROJECT_ID = environ.get("GCP_PROJECT_ID", "fallback")
GCP_RESULTS_BUCKET = environ.get("GCP_RESULTS_BUCKET", f"{GCP_PROJECT_ID}-prefect-results")
PYTHON_VERSION = ".".join(environ.get("PYTHON_VERSION", "3.10").split(".")[:2])
PREFECT_VERSION = environ.get("PREFECT_VERSION", "2.14.3")
DEPLOYMENT_NAME = f"{FLOW_NAME}_{TIER_ENVIRONMENT.replace('-', '_')}"
BLOCK_NAME = f'{FLOW_NAME}_{environ.get("GITHUB_REF", "dev")}'

def main():
    """Main function."""
    create_deployment()


def create_block():
    block = GitHub(
        reference=GITHUB_REF,
        repository="https://github.com/prefectcboyd/prefectcicd.git"
    )
    # block.get_directory("folder-in-repo") # specify a subfolder of repo
    block.save(BLOCK_NAME)
    return block

def create_deployment():
    """Create deployment."""
    print(f"Creating deployment {DEPLOYMENT_NAME}...")

    environment = {
        "WORK_POOL": WORK_POOL,
        "GCP_PROJECT_ID": GCP_PROJECT_ID,
        "GCP_RESULTS_BUCKET": GCP_RESULTS_BUCKET,
        "PREFECT_VERSION": PREFECT_VERSION,
        "PYTHON_VERSION": PYTHON_VERSION,
    }

    infra_overrides = {
        "env": environment
    }

    deployment = Deployment.build_from_flow(
        flow=hello_world,
        name=DEPLOYMENT_NAME,
        work_pool_name=WORK_POOL,
        work_queue_name="default",
        infra_overrides=infra_overrides,
        path="/",
        storage=create_block(),
        entrypoint=f"flow.py:{FLOW_NAME}",
    )
    uuid = deployment.apply()
    print(f"Saved deployment {DEPLOYMENT_NAME}: {uuid}")


if __name__ == "__main__":
    main()