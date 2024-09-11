import os
import sys
sys.path.append(os.path.abspath('.'))
import json
from langchain_community.tools.tavily_search import TavilySearchResults
from agent.Medical_Knowledgebase_Agent.kg_module import KGmodule
import datetime

kg_model = KGmodule()
# from rag_module import RAGModule
# rag_module = RAGModule()


def internet_search_function(query):
    daily = TavilySearchResults(max_results=5)
    try:
        ret = daily.invoke(input=query)
        print("搜索结果:{}".format(ret))
        print("\n")
        content_list = []
        for obj in ret:
            content_list.append(obj["content"])
        return "\n".join(content_list)
    except Exception as e:
        return "search error:{}".format(e)


def query_user_for_details(query_user):
    return query_user


def finish(answer):
    """结束对话并给出最终答案"""
    return answer


def RAG_addition(query):
    # RAG库知识添加
    kg_results_texts = kg_model.query(query)
    rag_results_texts = ""
    # rag_results_texts = rag_module.query(query)
    results_texts = kg_results_texts + "".join(rag_results_texts)
    return results_texts


def get_current_time():
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化当前日期和时间
    formatted_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # 返回格式化后的当前时间
    return f"当前时间：{formatted_time}。"


tools_info = [
    {
        "type": "function",
        "function": {
            "name": "query_user_for_details",
            "description": "当需要更多医学信息以提供个性化建议或解决方案时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "向用户提出的问题，旨在澄清或细化其医学需求。",
                    }
                },
            },
        "required": ["prompt"],
        },
    },
    {
        "type": "function",
        "function": {
            "name": "finish",
            "description": "结束对话并给出最终答案。",
            "parameters": {
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "string",
                        "description": "最终给出的答案，通常为对用户问题的回答或解决方案。",
                    }
                },
                },
        "required": ["answer"],
        },
    },
    {
        "type": "function",
        "function": {
            "name": "RAG_addition",
            "description": "使用构建的医学知识图谱提供疾病、症状、治疗方法等之间的详细关系和交互信息。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用户查询的复杂医学条目或概念，涉及系统性知识理解和条件关联的查询。",
                    }
                },
            },
        "required": ["query"],
        },
    },
    {
        "type": "function",
        "function": {
            "name": "internet_search_function",
            "description": "通过联网查询获取最新的医学研究成果、临床试验报告及全球卫生政策更新，特别适用于需要最新医学信息的查询。此功能能弥补知识图谱和现有内部数据的不足。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "需要了解最新科研成果或最新医学信息的查询，如新型疗法、新药上市信息或新兴病毒的防控措施。",
                    }
                },
            },
        "required": ["query"],
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "调用系统函数，返回现在的时间。在调用internet_search_function之前,如果用户的问题涉及到时间，首先需要调用get_current_time获得现在的时间。或者其他模块需要现在的时间。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "在调用internet_search_function之前,如果用户的问题涉及到时间，首先需要调用get_current_time获得现在的时间。或者其他模块需要现在的时间",
                    }
                },
            },
        "required": ["query"],
        },
    },
]


# 工具使用逻辑说明
action_logic = """ 
工具使用逻辑：
1. 当用户的问题涉及医学相关知识或健康情况时，首先调用RAG_addition模块。可以提供广泛而深入的信息。
2. 如果用户信息不完整或需要进一步澄清具体的医学状况或需求，使用query_user_for_details工具来询问用户详细情况。
3. 当所有医学信息收集完毕，并且问题得到充分回答时，使用finish工具确认用户满意并结束对话。
4. 如果用户的问题显然不涉及医学知识（例如，涉及法律、技术或其他领域），则直接返回一条消息：“您的问题似乎不涉及医学知识。请使用相应的专业工具或服务以获得最佳答案。”
5. 在调用internet_search_function之前,如果用户的问题涉及到时间，首先需要调用get_current_time获得现在的时间。并进行推断，随后进行下一步。
"""

# 工具映射逻辑
tools_map = {
    "internet_search_function": internet_search_function,
    "query_user_for_details": query_user_for_details,
    "RAG_addition": RAG_addition,
    "finish": finish,
    "get_current_time": get_current_time,
}


def gen_tools_desc():
    tools_desc = []

    # 遍历 tools_info 中的每个工具
    for idx, t in enumerate(tools_info):
        # 构建每个工具的参数描述，如果 t 中有 'parameters' 字段
        desc = t.get("function", {})

        # 构建工具的完整描述，包括名称、描述、参数
        tool_desc = {
            "name": desc["name"],
            "description": desc["description"],
            "parameters": desc["parameters"],
            "required": desc["required"],
        }

        # 将工具描述追加到 tools_desc 列表中
        tools_desc.append(tool_desc)

    # 将 tools_desc 转换为格式化的 JSON 字符串
    tools_prompt = json.dumps(tools_desc, ensure_ascii=False, indent=4)
    # 添加工具使用逻辑说明
    tools_prompt += "\n" + action_logic

    return tools_prompt
