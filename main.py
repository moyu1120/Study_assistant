import argparse

from core.loader import (
    load_problems,
    get_problem_by_id,
    get_problems_by_category,
    get_problems_by_category_and_difficulty,
)
from core.wrong_book import (
    add_wrong_question,
    get_wrong_questions,
    get_wrong_stats,
)
from core.vector_store import build_vector_store
from core.rag import ask_rag


def show_problem(problems, problem_id):
    problem = get_problem_by_id(problems, problem_id)
    if not problem:
        print("未找到该题目。")
        return

    print(f"题号: {problem['id']}")
    print(f"题目: {problem['title']}")
    print(f"难度: {problem['difficulty']}")
    print(f"类别: {', '.join(problem.get('categories', []))}")
    print("\n题目描述:")
    print(problem.get("description", ""))
    print("\n核心思路:")
    print(problem.get("idea", ""))
    print("\n代码:")
    print(problem.get("code", ""))


def recommend(problems, category, difficulty=None, num=3):
    if difficulty:
        result = get_problems_by_category_and_difficulty(problems, category, difficulty)
    else:
        result = get_problems_by_category(problems, category)

    if not result:
        print("没有找到符合条件的题目。")
        return

    title = f"推荐题目（类别: {category}"
    if difficulty:
        title += f", 难度: {difficulty}"
    title += "）:"
    print(title)

    for problem in result[:num]:
        print(f"- {problem['id']}. {problem['title']} ({problem['difficulty']})")


def add_wrong(problems, problem_id):
    problem = get_problem_by_id(problems, problem_id)
    if not problem:
        print("未找到该题目，无法加入错题集。")
        return

    item = add_wrong_question(problem)
    print("已加入错题集：")
    print(f"- {item['id']}. {item['title']} (错误次数: {item['wrong_count']})")


def show_wrong():
    wrong_questions = get_wrong_questions()
    if not wrong_questions:
        print("当前错题集为空。")
        return

    print("当前错题集：")
    for item in wrong_questions:
        print(
            f"- {item['id']}. {item['title']} "
            f"[{item['difficulty']}] "
            f"类别: {', '.join(item.get('categories', []))} "
            f"错误次数: {item['wrong_count']}"
        )


def show_wrong_stats():
    stats = get_wrong_stats()
    print(f"错题总次数: {stats['total_wrong']}")

    if not stats["category_count"]:
        print("暂无类别统计。")
        return

    print("按类别统计：")
    for category, count in stats["category_count"]:
        print(f"- {category}: {count}")


def build_index():
    build_vector_store()
    print("FAISS 索引构建完成。")


def ask_question(query, top_k=3, model_name="llama3"):
    answer = ask_rag(query=query, top_k=top_k, model_name=model_name)
    print(answer)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--task",
        required=True,
        choices=[
            "show_problem",
            "recommend",
            "add_wrong",
            "show_wrong",
            "wrong_stats",
            "build_index",
            "ask",
        ]
    )
    parser.add_argument("--id", type=int)
    parser.add_argument("--category", type=str)
    parser.add_argument("--difficulty", type=str)
    parser.add_argument("--num", type=int, default=3)
    parser.add_argument("--query", type=str)
    parser.add_argument("--model", type=str, default="llama3")

    args = parser.parse_args()

    problems = load_problems()

    if args.task == "show_problem":
        if args.id is None:
            print("请提供 --id")
            return
        show_problem(problems, args.id)

    elif args.task == "recommend":
        if args.category is None:
            print("请提供 --category")
            return
        recommend(problems, args.category, args.difficulty, args.num)

    elif args.task == "add_wrong":
        if args.id is None:
            print("请提供 --id")
            return
        add_wrong(problems, args.id)

    elif args.task == "show_wrong":
        show_wrong()

    elif args.task == "wrong_stats":
        show_wrong_stats()

    elif args.task == "build_index":
        build_index()

    elif args.task == "ask":
        if args.query is None:
            print("请提供 --query")
            return
        ask_question(args.query, args.num, args.model)


if __name__ == "__main__":
    main()