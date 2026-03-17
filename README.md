# Study Assistant

一个基于本地大语言模型与 RAG 检索流程构建的算法学习助手。

当前版本支持在命令行中完成算法题语义检索、题目推荐、错题记录与学习建议生成。系统整体采用本地部署方式，不依赖云端 API，后续可以扩展为 Web 应用、API 服务或 Agent 工具。

---

# 项目简介

本项目的目标是构建一个面向算法刷题场景的本地学习助手。

用户可以输入一道题目的自然语言描述，系统会通过向量检索找到最相近的题目，并结合本地大语言模型生成知识点判断、原因分析和练习建议。

当前项目已经实现了一套完整的基础 RAG 流程，包括：

* 题库解析
* 结构化数据构建
* 向量数据库索引
* 语义检索
* LLM 解释生成
* 错题管理

---

# 当前已实现功能

目前系统支持以下能力：

* 题库解析与结构化存储
* 基于分类的题目推荐
* 错题记录与统计
* 基于 FAISS 的语义检索
* 基于本地 LLM 的 RAG 问答解释
* CLI 命令行交互

示例功能包括：

* 输入题意，查找最相近的 Hot100 题目
* 返回题目对应的知识点、原因分析和建议练习方向
* 记录用户错题并进行简单统计

---

# 技术栈

本项目当前使用的主要技术如下：

* Python 3.10
* LangChain
* FAISS
* Ollama
* CLI 命令行交互

---

# 模块说明

### parser.py

用于解析 Markdown 格式的题库文件，并将原始题目信息转换为结构化 JSON 数据。

### loader.py

用于加载题库，并提供按照题目编号、类别等条件查询题目的能力。

### wrong_book.py

用于管理错题记录，包括添加错题、查看错题以及统计错题情况。

### documents.py

将结构化题库数据转换为 LangChain 所需的 `Document` 格式，作为后续 RAG 检索的输入。

### vector_store.py

负责构建 FAISS 向量数据库，实现题库的语义向量索引。

### rag.py

实现 RAG 检索与生成逻辑，包括相似题目查找、Prompt 构造以及本地 LLM 输出。

### main.py

当前项目的命令行入口，用于统一调用题库查询、推荐、错题管理和 RAG 问答等功能。

---

# 运行方式

### 1 创建并激活虚拟环境

请根据自己的系统环境创建 Python 3.10 虚拟环境。

### 2 安装依赖

将项目依赖安装到当前环境中。

### 3 准备本地模型

确保本地已经安装并运行 Ollama，并已拉取所需模型。

### 4 构建向量索引

首次运行前，需要先构建题库索引。

### 5 通过 CLI 调用功能

可以通过命令行执行题目查询、推荐或 RAG 问答功能。

---

# CLI 使用示例

### 语义检索问答

```bash
python main.py --task ask --query "给定数组，找三个数之和等于0"
```

### 查看题目

```bash
python main.py --task show_problem --id 1
```

### 分类推荐

```bash
python main.py --task recommend --category 双指针
```

### 添加错题

```bash
python main.py --task add_wrong --id 15
```

---

# 项目结构

```text
Study_assistant
│
├── core
│   ├── documents.py
│   ├── vector_store.py
│   ├── rag.py
│   ├── parser.py
│   ├── loader.py
│   └── wrong_book.py
│
├── data
│   ├── raw
│   │   ├── Hot100_Easy.md
│   │   ├── Hot100_Medium.md
│   │   └── class.md
│   │
│   └── processed
│       ├── problems.json
│       ├── categories.json
│       └── wrong_questions.json
│
└── main.py
```

---
