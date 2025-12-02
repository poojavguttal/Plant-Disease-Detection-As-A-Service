FROM python:3.10-slim

# System deps (Pillow libjpeg, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libjpeg62-turbo-dev zlib1g-dev libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Project working dir
WORKDIR /app

# Add requirements first for better cache
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src/ /app/src/
COPY notebooks/ /app/notebooks/
COPY configs/ /app/configs/

# (data will be mounted as a volume; don’t bake large data into image)
# Expose Jupyter
EXPOSE 8888

# Default command: Jupyter Lab for docs/demos
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser"]