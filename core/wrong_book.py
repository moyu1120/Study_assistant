import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
WRONG_FILE = PROCESSED_DIR / "wrong_questions.json"


def ensure_wrong_file():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    if not WRONG_FILE.exists():
        with open(WRONG_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)


def load_wrong_questions():
    ensure_wrong_file()
    with open(WRONG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_wrong_questions(data):
    with open(WRONG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_wrong_question(problem):
    wrong_questions = load_wrong_questions()

    for item in wrong_questions:
        if item["id"] == problem["id"]:
            item["wrong_count"] += 1
            save_wrong_questions(wrong_questions)
            return item

    new_item = {
        "id": problem["id"],
        "title": problem["title"],
        "difficulty": problem["difficulty"],
        "categories": problem.get("categories", []),
        "wrong_count": 1
    }

    wrong_questions.append(new_item)
    save_wrong_questions(wrong_questions)
    return new_item


def get_wrong_questions():
    return load_wrong_questions()


def get_wrong_stats():
    wrong_questions = load_wrong_questions()

    category_count = {}
    total_wrong = 0

    for item in wrong_questions:
        total_wrong += item["wrong_count"]
        for category in item.get("categories", []):
            category_count[category] = category_count.get(category, 0) + item["wrong_count"]

    sorted_categories = sorted(category_count.items(), key=lambda x: x[1], reverse=True)

    return {
        "total_wrong": total_wrong,
        "category_count": sorted_categories
    }


if __name__ == "__main__":
    ensure_wrong_file()
    data = get_wrong_questions()
    print("当前错题集：")
    print(data)

    stats = get_wrong_stats()
    print("\n错题统计：")
    print(stats)