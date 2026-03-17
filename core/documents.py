from langchain_core.documents import Document
from core.loader import load_problems


def problem_to_text(problem):
    return (
        f"题目: {problem.get('title', '')}\n"
        f"难度: {problem.get('difficulty', '')}\n"
        f"类别: {', '.join(problem.get('categories', []))}\n"
        f"题目描述: {problem.get('description', '')}\n"
        f"核心思路: {problem.get('idea', '')}"
    )


def build_problem_documents():
    problems = load_problems()
    docs = []

    for problem in problems:
        doc = Document(
            page_content=problem_to_text(problem),
            metadata={
                "id": problem["id"],
                "title": problem["title"],
                "difficulty": problem["difficulty"],
                "categories": problem.get("categories", []),
                "description": problem.get("description", ""),
                "idea": problem.get("idea", ""),
            }
        )

        docs.append(doc)

    return docs