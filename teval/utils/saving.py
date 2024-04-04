import tempfile
from pathlib import Path
import os
import pandas as pd
from composer.utils import maybe_create_object_store_from_uri, parse_uri


def to_cloud(df: pd.DataFrame, filename:str, upload_dir: str):

    _, _, path = parse_uri(upload_dir)
    object_store = maybe_create_object_store_from_uri(upload_dir)
    temp_file_name = None
    with tempfile.NamedTemporaryFile() as tmp_file:
        temp_file_name = tmp_file.name
        df.to_json(tmp_file, orient="records", lines=True)

        if object_store is not None:
            path_name = os.path.join(path, filename)
            path_name = path_name.replace("json", "jsonl")
            object_store.upload_object(path_name, temp_file_name)
        else:
            raise FileNotFoundError


def upload_results(in_dir, out_dir):
    """Upload all files at the top level of `in_dir` to `out_dir` in the cloud."""

    # Get all filepaths in the out directory; we will upload these files
    filenames = next(os.walk(in_dir))[2]
    filepaths = [os.path.join(in_dir, filename) for filename in filenames]

    for filepath, filename in zip(filepaths, filenames):
        df = pd.read_json(filepath).T
        to_cloud(df, filename, out_dir)

def download_results(in_dir, out_dir):
    """Download all files in `in_dir` from the cloud to `out_dir`. """

    _, _, path = parse_uri(in_dir)
    object_store = maybe_create_object_store_from_uri(in_dir)
    if object_store is not None:
        object_names = object_store.list_objects(path)
        for object_name in object_names:
            filename = object_name.split("/")[-1]
            out_path = os.path.join(out_dir, filename)
            object_store.download_object(object_name, out_path)
