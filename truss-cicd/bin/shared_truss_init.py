from truss.remote.remote_factory import RemoteConfig, RemoteFactory
from truss.truss_handle import TrussHandle
from tenacity import Retrying, stop_after_attempt, wait_random_exponential

REMOTE_NAME = "ci"
BASETEN_HOST = "https://app.baseten.co"

def write_trussrc_file(api_key: str):
    ci_user = RemoteConfig(
        name=REMOTE_NAME,
        configs={
            "api_key": api_key,
            "remote_url": BASETEN_HOST,
            "remote_provider": "baseten",
        },
    )
    RemoteFactory.update_remote_config(ci_user)

def deploy_truss(truss_handle: TrussHandle, publish: bool) -> str:
    remote_provider = RemoteFactory.create(remote=REMOTE_NAME)
    model_name = truss_handle.spec.config.model_name
    for _ in Retrying(
        wait=wait_random_exponential(multiplier=1, max=120),
        stop=stop_after_attempt(5),
        reraise=True,
    ):
        service = remote_provider.push(
            truss_handle, model_name, publish=publish, trusted=True
        )
        return service.model_version_id
