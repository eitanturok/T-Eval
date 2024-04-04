import shutil
import tempfile
from pathlib import Path
from typing import List

import pandas as pd
from composer.utils import maybe_create_object_store_from_uri, parse_uri


def upload_generations(
    generations: List[str], generations_save_folder: str, task_name: str, eval_name: str
):
    _, _, path = parse_uri(generations_save_folder)
    object_store = maybe_create_object_store_from_uri(generations_save_folder)
    temp_file_name = None
    with tempfile.NamedTemporaryFile() as tmp_file:
        temp_file_name = tmp_file.name
        df = pd.DataFrame(generations)

        df.to_json(tmp_file, orient="records", lines=True)

        if object_store is not None:
            path_name = path

            path_name += f"/{eval_name}/{task_name}/"

            object_store.upload_object(
                path_name + "generations.jsonl",
                temp_file_name,
            )
        else:
            actual_path = Path(path, eval_name, task_name, "generations.jsonl")
            actual_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(temp_file_name, actual_path)
