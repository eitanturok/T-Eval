import os
from typing import Optional

from huggingface_hub import snapshot_download


def add_suffix_to_filenames(directory, suffix):
    """Add suffix `suffix` to all the files in `directory`."""
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}{suffix}{ext}"
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))


def download_dataset(dataset_path: Optional[str] = None):

    print(dataset_path)

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

    # # the `T-eval` repo expects all filenames to end in "_suffix"
    # data_dir = cwd + "/data"
    # suffix = "_subset"
    # add_suffix_to_filenames(data_dir, suffix)

