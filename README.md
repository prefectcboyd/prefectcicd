# Prefect Build Workflow

This GitHub Actions workflow automates the deployment process for Python applications using Prefect Cloud. The workflow is designed to handle different environments (Production and Development) based on the branch where the changes are pushed.

Reviewing `.github/workflows`, there are two different possible GitHub actions, which match different triggers.  
This is intended to provide different Prefect deployment mechanisms (`.deploy()` and `.build_from_flow()`).

## Workflow Breakdown

### Environment Variables
The workflow uses several environment variables, including `PREFECT_API_KEY`, `PREFECT_API_URL`, `PROD_WORKSPACE`, and `DEV_WORKSPACE`. These are set as secrets in the repository settings for security.  
With the API key and URL set, a `prefect cloud login` is not necessary.  
Further, differentiating between workspaces (`dev` and `prod` or however your account is established) is only necessary if multiple workspaces are being utilized.  
Your workspaces can be determined via `prefect cloud workspace ls` and should be saved in the form like `chrisbprefectio/dev`.


*[Configuring API Settings](https://docs.prefect.io/latest/cloud/connecting/?h=api#manually-configure-prefect-api-settings)
*[Prefect Workspace Login](https://docs.prefect.io/latest/cloud/connecting/?h=api#change-workspaces)

### Trigger
There are two separate GitHub action workflows in this repository:
1. `prefect-deploy-prod` - intended to trigger on pushes to `main`, and uses `.build_from_flow` to deploy to Prefect.
2. `prefect-deploy-feature` - intended to trigger on pushes to `feature-*`, and uses `.deploy` to deploy to Prefect.


### Jobs
Both workflow contains a single job named `deploy`, which runs on the latest Ubuntu runner.

#### Steps:
1. **Check out repository**: The workflow checks out the code repository to make it accessible in the job.

2. **Set up Python 3.10**: Python 3.10 is set up for the job, along with pip caching, to speed up dependency installation.

3. **Install Dependencies**: Installs the required Python dependencies from `requirements.txt`.

4. **Environment-specific Actions**:
    - **Production Environment** (Main branch):
        - Switches to the production workspace using the `PROD_WORKSPACE` environment variable.
        - Executes `deployment.py` to deploy on every push to `main`.

    - **Development Environment** (Feature branches):
        - Switches to the development workspace using the `DEV_WORKSPACE` environment variable.
        - Checks for and runs all modified Python files in feature branches, to deploy to resolved branches.

### Environment Context
The `BRANCH_REF` environment variable is set dynamically to hold the reference of the branch where the workflow is running.
The `WORK_POOL` variable is added to environment variables to resolve which worker should retrieve flow runs at run time. `dev` and `prod` are used in this example, but these should be changed to reflect the work pools used in your environment.

## Usage
Push your changes to the appropriate branch (`main` for production, `feature-*` for development). The workflow will automatically handle the deployment process based on the branch context.

### Notes
- Ensure that the required secrets are set in the GitHub repository settings.
- The workflow is designed to be flexible and can be adapted to different Python-based deployment strategies with Prefect Cloud.
