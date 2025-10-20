import os, shutil, random, yaml
from pathlib import Path
from PIL import Image
from tqdm import tqdm
from sklearn.model_selection import train_test_split

RAW_DIR = Path("/app/data/raw/PlantVillage")
INTERIM_DIR = Path("/app/data/interim")
PROCESSED_DIR = Path("/app/data/processed")

def is_image(p: Path):
    return p.suffix.lower() in [".jpg", ".jpeg", ".png"]

def load_config():
    with open("/app/configs/classes.yaml", "r") as f:
        return yaml.safe_load(f)

def collect_class_paths(raw_dir: Path, crops):
    """
    Assumes PlantVillage structure like:
    PlantVillage/<ClassName>/*.jpg
    Where <ClassName> often contains crop + disease (e.g., 'Tomato___Early_blight').
    """
    class_dirs = []
    for d in raw_dir.iterdir():
        if d.is_dir() and any(d.name.startswith(c) for c in crops):
            class_dirs.append(d)
    return class_dirs

def copy_filtered(class_dirs):
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    for d in class_dirs:
        out = INTERIM_DIR / d.name
        out.mkdir(exist_ok=True, parents=True)
        for img in d.glob("*"):
            if is_image(img):
                dest = out / img.name
                if not dest.exists():
                    shutil.copy2(img, dest)

def resize_and_split(image_size, val_ratio, test_ratio, min_images=1):
    # Build class -> file list
    classes = sorted([p.name for p in INTERIM_DIR.iterdir() if p.is_dir()])
    splits = ["train","val","test"]
    for s in splits:
        (PROCESSED_DIR / s).mkdir(parents=True, exist_ok=True)

    for cls in classes:
        files = [p for p in (INTERIM_DIR/cls).iterdir() if is_image(p)]
        if len(files) < min_images:
            print(f"Skipping {cls}: only {len(files)} images")
            continue

        train_files, tmp = train_test_split(files, test_size=(val_ratio+test_ratio), random_state=42, shuffle=True)
        rel = test_ratio/(val_ratio+test_ratio) if (val_ratio+test_ratio) > 0 else 0
        val_files, test_files = train_test_split(tmp, test_size=rel, random_state=42, shuffle=True)

        for subset, subset_files in [("train", train_files), ("val", val_files), ("test", test_files)]:
            out_dir = PROCESSED_DIR / subset / cls
            out_dir.mkdir(parents=True, exist_ok=True)
            for src in tqdm(subset_files, desc=f"{cls}:{subset}"):
                try:
                    img = Image.open(src).convert("RGB")
                    img = img.resize((image_size, image_size), Image.BILINEAR)
                    # normalization usually happens at training time; we store resized RGB
                    img.save(out_dir / src.name, quality=95)
                except Exception as e:
                    print("Bad image:", src, e)

def main():
    cfg = load_config()
    crops = cfg["include_crops"]
    class_dirs = collect_class_paths(RAW_DIR, crops)
    print(f"Selected classes ({len(class_dirs)}):", [d.name for d in class_dirs])
    copy_filtered(class_dirs)
    resize_and_split(
        image_size=cfg["image_size"],
        val_ratio=cfg["val_ratio"],
        test_ratio=cfg["test_ratio"],
        min_images=cfg.get("min_images_per_class", 1)
    )
    print("Done. Processed data at:", PROCESSED_DIR)
    # Generate a report
    os.system("python /app/src/make_preprocessing_report.py")

if __name__ == "__main__":
    main()
