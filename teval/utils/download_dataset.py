import os
from typing import Optional

from huggingface_hub import snapshot_download


def download_dataset(dataset_path: Optional[str] = None):

    # if `None`, download all the files in the `data` directory on HF
    if dataset_path is None:
        dataset_path = "data/*"

    # get cwd
    cwd = os.getcwd()

    # download the dataset from HF with `snapshot_download`
    # because there are errors downloading with `load_dataset`
    snapshot_download(
        repo_id="lovesnowbest/T-Eval",
        repo_type="dataset",
        local_dir=cwd,
        allow_patterns=dataset_path,
        local_dir_use_symlinks=False
        )
