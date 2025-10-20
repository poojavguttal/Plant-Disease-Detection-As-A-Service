## Overview
A containerized, service-oriented project that uses a Convolutional Neural Network (CNN) to detect crop leaf diseases from images.  
Trained on the PlantVillage dataset and deployed via a REST API for web/mobile clients.

## Features
- Dockerized environment (Linux-compatible)
- Preprocessing pipeline (resize 224×224, normalization, dataset split)
- Auto-generated Jupyter report
- Custom CNN training and cloud deployment ready


# Make sure to install Docker and switch to Linux containers in the settings 

# 1) Build & run Jupyter container
docker compose up --build

# 2) (In another terminal) Run preprocessing
docker compose exec dev python /app/src/preprocess.py

# 3) Open Jupyter: http://localhost:8888 (token printed in logs)
# 4) View notebook: notebooks/01_preprocessing.ipynb