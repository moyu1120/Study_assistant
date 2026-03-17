from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from core.vector_store import load_vector_store


def format_doc(doc, rank):
    m = doc.metadata

    return (
        f"[候选题目 {rank}]\n"
        f"题号: {m.get('id')}\n"
        f"标题: {m.get('title')}\n"
        f"难度: {m.get('difficulty')}\n"
        f"类别: {', '.join(m.get('categories', []))}\n"
        f"题目描述: {m.get('description')}\n"
        f"核心思路: {m.get('idea')}\n"
    )


def build_context(docs):
    parts = []
    for i, doc in enumerate(docs, start=1):
        parts.append(format_doc(doc, i))
    return "\n".join(parts)


def create_chain(model_name="llama3"):
    prompt = PromptTemplate.from_template(
        """
你是一名算法学习助手。

请根据用户输入的题意描述，以及候选题目，判断最接近的 LeetCode / Hot100 题。用中文回答。

输出格式：

最接近的题目：
知识点判断：
原因分析：
建议练习：

用户输入：
{query}

候选题目：
{context}
"""
    )

    llm = ChatOllama(
        model=model_name,
        temperature=0.2,
    )

    return prompt | llm


def ask_rag(query, top_k=3, model_name="llama3"):
    vector_store = load_vector_store()

    docs = vector_store.similarity_search(query, k=top_k)

    if not docs:
        return "没有找到相似题目。"

    context = build_context(docs)

    chain = create_chain(model_name)

    result = chain.invoke({
        "query": query,
        "context": context
    })

    if hasattr(result, "content"):
        return result.content

    return str(result)