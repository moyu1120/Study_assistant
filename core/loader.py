import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROBLEMS_FILE = PROCESSED_DIR / "problems.json"
CATEGORIES_FILE = PROCESSED_DIR / "categories.json"


def load_problems(filepath=PROBLEMS_FILE):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def load_categories(filepath=CATEGORIES_FILE):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def get_problem_by_id(problems, problem_id):
    for problem in problems:
        if problem["id"] == problem_id:
            return problem
    return None


def get_problem_by_title(problems, title):
    title = title.strip().lower()
    for problem in problems:
        if problem["title"].strip().lower() == title:
            return problem
    return None


def get_problems_by_category(problems, category):
    result = []
    for problem in problems:
        if category in problem.get("categories", []):
            result.append(problem)
    return result


def get_problems_by_difficulty(problems, difficulty):
    difficulty = difficulty.strip().lower()
    result = []
    for problem in problems:
        if problem.get("difficulty", "").lower() == difficulty:
            result.append(problem)
    return result


def get_problems_by_category_and_difficulty(problems, category, difficulty):
    difficulty = difficulty.strip().lower()
    result = []
    for problem in problems:
        if category in problem.get("categories", []) and problem.get("difficulty", "").lower() == difficulty:
            result.append(problem)
    return result


if __name__ == "__main__":
    problems = load_problems()
    categories = load_categories()

    print(f"题目总数: {len(problems)}")
    print(f"类别总数: {len(categories)}")

    p1 = get_problem_by_id(problems, 1)
    print("\n按题号查找 id=1:")
    print(p1["title"] if p1 else "未找到")

    p2 = get_problem_by_title(problems, "移动零")
    print("\n按标题查找 移动零:")
    print(p2["id"] if p2 else "未找到")

    hash_problems = get_problems_by_category(problems, "哈希")
    print(f"\n哈希类题目数量: {len(hash_problems)}")

    easy_problems = get_problems_by_difficulty(problems, "easy")
    print(f"\neasy 题目数量: {len(easy_problems)}")

    two_pointer_easy = get_problems_by_category_and_difficulty(problems, "双指针", "easy")
    print(f"\n双指针 easy 题数量: {len(two_pointer_easy)}")