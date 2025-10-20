# /app/src/make_preprocessing_report.py

import json
import random
from pathlib import Path
from textwrap import dedent

import nbformat as nbf
from nbclient import NotebookClient

# -------------------------------------------------------------------
# Paths inside the Docker container
# -------------------------------------------------------------------
DATA_ROOT = Path("/app/data/processed")                # expects train/ val/ test/ subfolders
NOTEBOOK_OUT = Path("/app/notebooks/01_preprocessing.ipynb")

# -------------------------------------------------------------------
# Helpers (robust to case + nesting)
# -------------------------------------------------------------------
IMG_EXTS = {".jpg", ".jpeg", ".png"}


def is_img(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in IMG_EXTS


def find_classes(split_dir: Path):
    if not split_dir.exists():
        return []
    return sorted([p.name for p in split_dir.iterdir() if p.is_dir()])


def count_images(split_dir: Path):
    """
    Count images per class, recursively and case-insensitively.
    Returns dict {class_name: count}.
    """
    counts = {}
    if not split_dir.exists():
        return counts
    for cls in find_classes(split_dir):
        cls_dir = split_dir / cls
        counts[cls] = sum(1 for p in cls_dir.rglob("*") if is_img(p))
    return counts


def sample_images(split_dir: Path, n=6):
    """
    Return up to n image paths (strings) sampled across classes recursively.
    """
    imgs = []
    if split_dir.exists():
        for cls in find_classes(split_dir):
            imgs.extend([p for p in (split_dir / cls).rglob("*") if is_img(p)])
    random.shuffle(imgs)
    return [str(p) for p in imgs[:n]]


# -------------------------------------------------------------------
# Notebook cell builders
# -------------------------------------------------------------------
def _mk_md_cell(md: str):
    return nbf.v4.new_markdown_cell(md)


def _mk_code_cell(code: str):
    return nbf.v4.new_code_cell(code)


# -------------------------------------------------------------------
# Build the notebook (structure + code/markdown cells)
# -------------------------------------------------------------------
def build_notebook():
    nb = nbf.v4.new_notebook()
    nb["cells"] = []

    # Title & intro
    nb["cells"] += [
        _mk_md_cell("# PlantVillage Preprocessing Report"),
        _mk_md_cell(
            "This notebook was **auto-generated** after running the preprocessing pipeline. "
            "It documents dataset structure, class counts, sample images, and the train/val/test split."
        ),
        _mk_md_cell("**Data root:** `/app/data/processed`  \n**Target size:** 224×224  \n**Splits:** train / val / test"),
    ]

    # Quick path debug cell
    nb["cells"] += [
        _mk_md_cell("## Environment Check (paths & splits)"),
        _mk_code_cell(dedent("""\
            from pathlib import Path
            DATA_ROOT = Path('/app/data/processed')
            print('Data root:', DATA_ROOT)
            if not DATA_ROOT.exists():
                print('WARNING: data root does not exist.')
            splits = [p.name for p in DATA_ROOT.iterdir() if p.is_dir()] if DATA_ROOT.exists() else []
            print('Splits found:', splits)
            for split in ['train', 'val', 'test']:
                p = DATA_ROOT / split
                if p.exists():
                    classes = sorted([d.name for d in p.iterdir() if d.is_dir()])
                    print(f'{split} classes ({len(classes)}):', classes[:10], '...' if len(classes) > 10 else '')
                else:
                    print(split, 'missing')
        """))
    ]

    # Imports used by later code cells
    nb["cells"] += [
        _mk_md_cell("## Imports"),
        _mk_code_cell(dedent("""\
            import json
            import pandas as pd
            import matplotlib.pyplot as plt
            from pathlib import Path
            from PIL import Image

            %matplotlib inline
            DATA_ROOT = Path('/app/data/processed')
        """)),
    ]

    # Compute counts on the Python side (this script), then pass as dicts to the notebook
    counts_train = count_images(DATA_ROOT / "train")
    counts_val = count_images(DATA_ROOT / "val")
    counts_test = count_images(DATA_ROOT / "test")

    nb["cells"] += [
        _mk_md_cell("## Class Counts (Train / Val / Test)"),
        _mk_code_cell(dedent(f"""\
            # dicts injected by the generator (this script)
            train_counts = {json.dumps(counts_train, indent=2)}
            val_counts   = {json.dumps(counts_val, indent=2)}
            test_counts  = {json.dumps(counts_test, indent=2)}

            # Build a single DataFrame (missing classes -> 0)
            df = pd.DataFrame({{
                'train': train_counts,
                'val': val_counts,
                'test': test_counts
            }}).fillna(0).astype(int)

            # Sort columns alphabetically for readability
            df = df.sort_index()
            df
        """)),
        _mk_md_cell("### Bar Chart (Per-class counts by split)"),
        _mk_code_cell(dedent("""\
            ax = df.plot(kind='bar', figsize=(12, 5))
            ax.set_xlabel('Class')
            ax.set_ylabel('Image count')
            ax.set_title('Per-class image counts by split')
            plt.tight_layout()
            plt.show()
        """)),
    ]

    # Random samples display (train)
    samples_train = sample_images(DATA_ROOT / "train", n=6)
    nb["cells"] += [
        _mk_md_cell("## Sample Images (Train)"),
        _mk_code_cell(dedent(f"""\
            samples = {json.dumps(samples_train, indent=2)}
            from pathlib import Path
            for p in samples:
                try:
                    img = Image.open(p).convert('RGB')
                    plt.figure(figsize=(3,3))
                    plt.imshow(img)
                    plt.title(Path(p).parent.name)
                    plt.axis('off')
                    plt.show()
                except Exception as e:
                    print('Could not open', p, e)
        """)),
    ]

    # Split summary derived from df (robust and simple)
    nb["cells"] += [
        _mk_md_cell("## Split Summary"),
        _mk_code_cell(dedent("""\
            summary = pd.DataFrame({
                'split': ['train', 'val', 'test'],
                'count': [df['train'].sum(), df['val'].sum(), df['test'].sum()]
            })
            summary
        """)),
        _mk_code_cell(dedent("""\
            ax = summary.set_index('split').plot(kind='bar', figsize=(5,3), legend=False)
            ax.set_ylabel('Images')
            ax.set_title('Total images by split')
            plt.tight_layout()
            plt.show()
        """)),
    ]

    # Notes
    nb["cells"] += [
        _mk_md_cell("## Notes"),
        _mk_md_cell(
            "- Images were resized to **224×224** during preprocessing.\n"
            "- **Normalization** (mean/std) is applied at **training time** in the dataloader.\n"
            "- Shown classes reflect filtered crops (e.g., Tomato / Potato / Corn).\n"
            "- This notebook is **auto-generated**; re-run the report script to refresh after dataset changes."
        ),
    ]

    return nb

# -------------------------------------------------------------------

# Save + execute the notebook

# -------------------------------------------------------------------

def save_and_execute(nb):

    NOTEBOOK_OUT.parent.mkdir(parents=True, exist_ok=True)

    # Save unexecuted notebook first

    nbf.write(nb, NOTEBOOK_OUT)



    # Execute to populate outputs (tables, plots, sample images)

    client = NotebookClient(nb, timeout=1200, kernel_name="python3", allow_errors=True)

    executed = client.execute()



    # Save executed notebook

    nbf.write(executed, NOTEBOOK_OUT)

    print(f"[REPORT] Wrote executed notebook to: {NOTEBOOK_OUT}")





def main():
    nb = build_notebook()
    save_and_execute(nb)





if __name__ == "__main__":

    main()
