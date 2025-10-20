# Make sure to install Docker and switch to Linux containers in the settings 

# 1) Build & run Jupyter container
docker compose up --build

# 2) (In another terminal) Run preprocessing
docker compose exec dev python /app/src/preprocess.py

# 3) Open Jupyter: http://localhost:8888 (token printed in logs)
# 4) View notebook: notebooks/01_preprocessing.ipynb