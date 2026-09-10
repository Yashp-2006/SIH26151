import os
from dotenv import load_dotenv
from huggingface_hub import hf_hub_download
import datasets
import json

load_dotenv()

def load_sample_file(filename: str) -> str:
    token = os.environ.get("HF_TOKEN")
    repo = os.environ.get("HF_DATASET_REPO")
    return hf_hub_download(repo_id=repo, filename=filename, repo_type="dataset", token=token)

def load_ground_truth() -> dict:
    local_path = load_sample_file("synthetic_ground_truth.json")
    with open(local_path, "r", encoding="utf-8") as f:
        return json.load(f)
