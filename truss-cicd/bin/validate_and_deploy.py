import argparse
import time
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from truss.cli.cli import _get_truss_from_directory
from shared_truss_init import BASETEN_HOST, deploy_truss, write_trussrc_file

@retry(wait=wait_fixed(60), stop=stop_after_attempt(20), reraise=True)
def attempt_inference(truss_handle, model_version_id, api_key):
    """
    Retry every 20 seconds to call inference on the example. Time out after 200 seconds.
    """

    print("Started attempt inference")
    example_model_input = {"text": "This is a test"}
    url = f"{BASETEN_HOST}/model_versions/{model_version_id}/predict"
    headers = {"Authorization": f"Api-Key {api_key}"}
    response = requests.post(url, headers=headers, json=example_model_input, timeout=30)
    print(response.content)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")


def push(api_key: str, target_directory: str, publish: bool = False, try_inference: bool = True):
    write_trussrc_file(api_key)
    truss_handle = _get_truss_from_directory(target_directory)
    model_version_id = deploy_truss(truss_handle, publish = publish)
    print(f"Deployed Truss {model_version_id}")
    if try_inference:
        time.sleep(20)
        attempt_inference(truss_handle, model_version_id, api_key)


def get_parser():
    parser = argparse.ArgumentParser(description="Deploy and optionally test a Truss model.")
    parser.add_argument("api_key", help="Baseten API key for authentication")
    parser.add_argument("target_directory", help="Target directory where Truss is located")
    parser.add_argument("--publish", action="store_true", help="Flag to publish the model")
    parser.add_argument("--attempt-inference", dest="attempt_inf", action="store_true", help="Attempt inference after deployment")
    parser.set_defaults(attempt_inf=True)
    return parser

def main(args):
    push(args.api_key, args.target_directory, args.publish, args.attempt_inf)

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)
