
import json
from pathlib import Path

import matplotlib.pyplot as plt


PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "evidence"
OUTPUT_DIR.mkdir(exist_ok=True)

RUNS = {
    "Real": "m1-real",
    "Oversampling": "m1-oversample",
    "Augmentation": "m1-augment",
    "Strong augmentation": "m1-augment-strong",
}

M2_RUNS = {
    "Base": "m2-base",
    "Guidance 2": "m2-guidance2",
    "Guidance 15": "m2-guidance15",
    "Steps 10": "m2-steps10",
}


def load_results():
    results = {}

    for label, run_name in RUNS.items():
        path = PROJECT_DIR / "runs" / run_name / "results.json"

        with open(path, encoding="utf-8") as file:
            data = json.load(file)

        results[label] = sorted(
            data["seeds"],
            key=lambda item: item["seed"]
        )

    return results


def create_plot(results, metric, title, filename):
    plt.figure(figsize=(10, 6))

    for label, records in results.items():
        seeds = [record["seed"] for record in records]
        values = [record[metric] for record in records]

        plt.plot(seeds, values, marker="o", label=label)

    plt.title(title)
    plt.xlabel("Random seed")
    plt.ylabel("Score")
    plt.xticks([0, 1, 2, 3, 4])
    plt.ylim(0, 1)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()

    output_path = OUTPUT_DIR / filename
    plt.savefig(output_path, dpi=150)
    plt.close()

    print("Saved:", output_path)


results = load_results()

create_plot(
    results,
    "egyptian_mau_recall",
    "Egyptian Mau Recall - Validation",
    "m1_recall.png"
)

create_plot(
    results,
    "macro_f1",
    "Macro-F1 - Validation",
    "m1_macro_f1.png"
)

print("Both plots generated successfully.")

# Meeting 2 — synthetic image generation

original_runs = RUNS.copy()

RUNS.clear()
RUNS.update(M2_RUNS)

m2_results = load_results()

create_plot(
    m2_results,
    "egyptian_mau_recall",
    "Meeting 2 - Egyptian Mau Recall (Validation)",
    "m2_recall.png"
)

create_plot(
    m2_results,
    "macro_f1",
    "Meeting 2 - Macro-F1 (Validation)",
    "m2_macro_f1.png"
)

RUNS.clear()
RUNS.update(original_runs)
