# Truss CI/CD Example 

This repository demonstrates how to integrate a Truss ML model into a CI/CD pipeline using GitHub Actions. 

Note that this is a toy example, and a production deploy should consider some of the following:
* Cost of running the github action while waiting for the model to be available
* In the case where a production build is generated, note that this example will not stop a previous build

## Structure

- `.github/workflows/truss-deployment.yml`: Defines the GitHub Actions workflow for testing, deploying, and promoting the Truss model. It includes steps for setting up the Python environment, installing dependencies, running tests, and executing the deployment script. Note that this will not deploy the model to production, only generate a production-ready image. To deploy, replace references to `--publish` with `--promote`
- `bin/validate_and_deploy.py`: A Python script that handles the deployment of the Truss model to Baseten and optionally attempts inference to ensure the model is working as expected.
- `bin/shared_truss_init.py`: Contains utility functions for configuring the deployment environment and deploying the Truss model to Baseten.
- `cicd/model/model.py`: The Truss model implementation, including the model class with `load` and `predict` methods.
- `cicd/tests/test_example.py`: A placeholder for model validation tests. It should be replaced with actual tests that verify the model's functionality before deployment.

The CI/CD pipeline is triggered by push or pull request events to the `develop` or `main` branches, with specific paths (`cicd/**`) being monitored for changes.

Ensure to set the necessary secrets (`TRUSS_API_KEY`) in your GitHub repository settings for authentication with Baseten and Truss services.


## Usage
To deploy and validate the model, push changes to the `model/` directory and the CI/CD pipeline will automatically handle testing, deployment, and validation.
Ensure your github environment has the apprpriate API key set as a secret
