import json
import os
from pathlib import Path

# Абсолютный путь к allure-results на уровень выше скрипта
ALLURE_RESULTS_DIR = (Path(__file__).parent / ".." / "allure-results").resolve()


def parse_allure_results(directory=ALLURE_RESULTS_DIR):
    results = []

    for file in os.listdir(directory):
        if not file.endswith("-result.json"):
            continue
        path = os.path.join(directory, file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        test_name = data.get("name")
        status = data.get("status")
        status_details = data.get("statusDetails", {})
        message = status_details.get("message", "")
        trace = status_details.get("trace", "")
        attachments = [
            att.get("source") for att in data.get("attachments", [])
        ]

        results.append({
            "name": test_name,
            "status": status,
            "message": message,
            "trace": trace,
            "attachments": attachments
        })

    return results


if __name__ == "__main__":
    parsed = parse_allure_results()
    for r in parsed:
        print(f"Test: {r['name']}, Status: {r['status']}")
        if r["status"] != "passed":
            print(f"  Message: {r['message']}")
            print(f"  Trace: {r['trace']}")
            if r["attachments"]:
                print(f"  Attachments: {r['attachments']}")
        print("-" * 50)
