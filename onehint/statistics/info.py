import json
from collections import defaultdict

from onehint import checkers
from onehint.main import versions_info


def analyze_versions():
    with open("../../datasets/data.json", "r") as f:
        data = json.load(f)
    correct = defaultdict(int)
    all_pairs = defaultdict(int)
    for record in data:
        record_results = []
        for version_info in versions_info():
            version = version_info.version
            module = getattr(checkers, f"v{version}")
            api_version = getattr(module, f"APIv{version}")
            response = api_version().find_duplicates(list(record.keys()))
            expected_response = list(record.values())
            for (response_pair, expected_pair) in zip(response, expected_response):
                correct[version] += len(expected_response) - len(set(response_pair).symmetric_difference(set(expected_pair))) - 1
                all_pairs[version] += len(expected_response) - 1
            record_results.append((response, response == expected_response))
        if not all(x == record_results[0] for x in record_results):
            print(record, [r[0] for r in record_results], [r[1] for r in record_results])
    for key in all_pairs:
        correct[key] //= 2
        all_pairs[key] //= 2
    for key in all_pairs:
        print(key, correct[key])


if __name__ == "__main__":
    analyze_versions()
