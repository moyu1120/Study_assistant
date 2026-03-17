import re
import json
from pathlib import Path


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def parse_problem_file(filepath, difficulty):
    """
    解析 Hot100_Easy.md 或 Hot100_Medium.md
    """
    text = filepath.read_text(encoding="utf-8")

    # 按题目切分
    blocks = re.split(r"### \[", text)[1:]

    problems = []

    for block in blocks:
        # 提取题号和标题
        header_match = re.match(r"(\d+)\.\s*([^\]]+)\]", block)
        if not header_match:
            continue

        problem_id = int(header_match.group(1))
        title = header_match.group(2).strip()

        # 提取题目描述
        desc_match = re.search(
            r"#### 题目描述\s*(.*?)\s*#### 核心思路",
            block,
            re.S
        )

        description = desc_match.group(1).strip() if desc_match else ""

        # 提取核心思路
        idea_match = re.search(
            r"#### 核心思路\s*(.*?)\s*#### 代码",
            block,
            re.S
        )

        idea = idea_match.group(1).strip() if idea_match else ""

        # 提取代码
        code_match = re.search(
            r"```python\s*(.*?)```",
            block,
            re.S
        )

        code = code_match.group(1).strip() if code_match else ""

        problems.append({
            "id": problem_id,
            "title": title,
            "difficulty": difficulty,
            "description": description,
            "idea": idea,
            "code": code,
            "categories": []
        })

    return problems


def parse_class_file(filepath):
    """
    解析 class.md，提取类别 -> 题号
    """
    text = filepath.read_text(encoding="utf-8")

    categories = {}
    current_category = None

    lines = text.splitlines()

    for line in lines:
        # 类别标题
        if line.startswith("## "):
            current_category = line.replace("## ", "").strip()
            categories[current_category] = []

        # 表格行
        match = re.search(r"\|\s*\S+\s*\|\s*(\d+)\s*\|", line)

        if match and current_category:
            pid = int(match.group(1))
            categories[current_category].append(pid)

    return categories


def attach_categories(problems, categories):
    """
    把类别信息挂到每道题上
    """
    id_to_problem = {p["id"]: p for p in problems}

    for category, ids in categories.items():
        for pid in ids:
            if pid in id_to_problem:
                id_to_problem[pid]["categories"].append(category)

    return problems


def save_json(data, filepath):
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    easy_file = RAW_DIR / "Hot100_Easy.md"
    medium_file = RAW_DIR / "Hot100_Medium.md"
    class_file = RAW_DIR / "Class.md"

    problems = []

    problems += parse_problem_file(easy_file, "easy")
    problems += parse_problem_file(medium_file, "medium")

    categories = parse_class_file(class_file)

    problems = attach_categories(problems, categories)

    save_json(problems, PROCESSED_DIR / "problems.json")
    save_json(categories, PROCESSED_DIR / "categories.json")

    print("Parsing finished.")
    print(f"Total problems: {len(problems)}")


if __name__ == "__main__":
    main()