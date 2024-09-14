import json
from collections import defaultdict

from onehint import main
from onehint.main import versions_info, RoundWords


def analyze_versions():
    with open("../../datasets/data.json", "r") as f:
        data = json.load(f)
    stats = defaultdict(int)
    for record in data:
        record_results = []
        for version_info in versions_info():
            version = version_info.version
            f = getattr(main, f"find_duplicates_v{version}")
            response = f(RoundWords(words=list(record.keys())))
            expected_response = list(record.values())
            if response.words == expected_response:
                stats[version] += 1
            record_results.append(response.words == expected_response)
        if not all(x == record_results[0] for x in record_results):
            print(record, record_results)
    for key in stats:
        print(key, stats[key] / len(data))


if __name__ == "__main__":
    analyze_versions()
