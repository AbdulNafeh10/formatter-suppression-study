"""Small discovery probe using the Phase 1 measurement code, before matching.

Every candidate and outcome is retained; these are not the main dataset.
"""

import json
from suppression_study.pipeline import ROOT, measure, save_json

CANDIDATES = {
    "semicolon": "x=missing_a; y=missing_b  # noqa: F821\n",
    "list_inline": "x = [missing_a,  # noqa: F821\n     missing_b]\n",
    "call_open": "print(  # noqa: F821\n    missing_a)\n",
    "list_closing": "x = [\n    missing_a,\n    missing_b\n]  # noqa: F821\n",
    "import_inline": "from os import (\n    path,  # noqa: F401\n    getcwd,\n)\n",
    "local_semicolon": "def f():\n    a=1; b=2  # noqa: F841\n",
    "repeated_name": "x=missing; y=missing  # noqa: F821\n",
    "unicode": "é=absent; λ=missing  # noqa: F821\n",
}


def main():
    directory = ROOT / "datasets" / "results" / "phase2-probes"
    directory.mkdir(parents=True, exist_ok=False)
    save_json(directory / "candidates.json", CANDIDATES)
    results = []
    for name, source in CANDIDATES.items():
        for formatter in ("black", "ruff"):
            result = measure(
                source,
                directory / f"{name}-{formatter}",
                formatter=formatter,
                dataset_origin="phase2-exploratory-probe",
                ai_assisted=True,
            )
            results.append(result)
            print(name, formatter, result.get("counts"), result["error"])
    (directory / "results.jsonl").write_text(
        "".join(json.dumps(result) + "\n" for result in results), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
