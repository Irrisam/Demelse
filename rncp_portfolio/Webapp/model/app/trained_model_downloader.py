import os
import subprocess

BUCKET = "demelse-models-2025"
REMOTE_PATH = "trained_models"
LOCAL_PATH = "rncp_portfolio/Webapp/model/app/trained_models"

os.makedirs(LOCAL_PATH, exist_ok=True)

files = [
    "USER_SERVICE_TRAINING_cosine.joblib",
    "USER_ETAB_TRAINING_cosine.joblib",
    "CONTENT_SERVICE_TRAINING_cosine.joblib",
    "CONTENT_RYTHME_TRAINING_cosine.joblib",
    "CONTENT_ETAB_TRAINING_cosine.joblib"
]

for f in files:
    remote = f"gs://{BUCKET}/{REMOTE_PATH}/{f}"
    local = os.path.join(LOCAL_PATH, f)
    print(f"Téléchargement de {f}...")
    subprocess.run(["gsutil", "cp", remote, local], check=True)
