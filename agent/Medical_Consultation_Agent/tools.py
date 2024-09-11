import sys
import os
sys.path.append(os.path.abspath('.'))
import json
import datetime
from agent.Medical_Knowledgebase_Agent.main import Medical_Knowledgebase_Agent

mka_agent = Medical_Knowledgebase_Agent()





def medical_knowledgebase_agent(query):
    medical_knowledgebase_result = mka_agent.agent_execute(query, max_request_time=5,debug=True)
    return medical_knowledgebase_result
def query_user_for_details(query_user):
    return query_user
def finish(answer):
    """ 结束对话并给出最终答案 """
    return answer



qa_pairs = [
    {"乳腺癌的症状有哪些？"},
    {"最近老流鼻涕怎么办？"},
    { "为什么有的人会失眠？"},
    { "失眠有哪些并发症？"},
    {"失眠的人不要吃啥？"},
    {"耳鸣了吃点啥？"},
    {"哪些人最好不好吃蜂蜜？"},
    { "鹅肉有什么好处？"},
    {"肝病要吃啥药？"},
    { "板蓝根颗粒能治啥病？"},
    { "脑膜炎怎么才能查出来？"},
    {"全血细胞计数能查出啥来？"},
    { "怎样才能预防肾虚？"},
    {"感冒要多久才能好？"},
    {"高血压要怎么治？"},
    {"白血病能治好吗？"},
    {"什么人容易得高血压？"},
    {"糖尿病的描述？"}
]

final_answer = {
    "患者信息": {
        "姓名": "",
        "性别": "",
        "年龄": "",
        "身高": "",
        "体重": ""
    },
    "主诉": "",
    "初步诊断": {
        "可能的疾病": []
    },
    "检查建议": [],
    "治疗建议": {
        "药物治疗": [],
        "生活方式建议": []
    },
    "健康管理建议": "",
    "紧急情况提示": ""
}

tools_info = [
    {
        "type": "function",
        "function": {
            "name": "query_user_for_details",
            "description": "当需要更多用户信息以提供具体建议或解决方案时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "向用户提出的问题，旨在澄清或细化其医学需求。"
                    }
                }
            },
            "required": ["prompt"]
        }
    },
    {
        "type": "function",
        "function": {
            "name": "finish",
            "description": "在医学咨询完成并确认用户满意后，结束对话并提供最终答案.",
            "parameters": {
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "dict",
                        "description": f"提供完整的医学问答信息。最终答案为json格式，如下{final_answer}。"
                    }
                }
            },
            "required": ["answer"]
        }
    },
    {
        "type": "function",
        "function": {
            "name": "medical_knowledgebase_agent",
            "description": "接受问句类型的提问，如果需要具体的药物，具体的症状等，调用医疗知识库，返回相关的医疗知识。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "接受问句类型的提问，如果需要具体的药物，具体的症状等，提供相关的医疗知识。"
                    }
                }
            },
            "required": ["query"]
        }
    }
]


# 工具使用逻辑说明
action_logic = f"""工具使用逻辑：
1. medical_knowledgebase_agent所能接受的query格式严格按照{qa_pairs}中的例子的风格进行提问，注意一定按照里面的例子风格进行提问，最好是问句。
2. 如果用户信息不完整或需要进一步澄清具体的需求，使用query_user_for_details工具来询问用户详细情况。
"""
# """ 
# 工具使用逻辑：
# 1. 当用户的问题需要涉及医学相关知识或健康情况时，调用medical_knowledgebase_agent模块。可以提供广泛而深入的信息。
# 2. 如果用户信息不完整或需要进一步澄清具体的需求，使用query_user_for_details工具来询问用户详细情况。
# 3. 当所有医学信息收集完毕，并且问题得到充分问诊建议回答时，使用finish工具确认用户满意并结束对话。
# """

# 工具映射逻辑
tools_map = {
    "query_user_for_details": query_user_for_details,
    "medical_knowledgebase_agent": medical_knowledgebase_agent,
    "finish":finish,
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

if __name__ == "__main__":
    tools_prompt = gen_tools_desc()
    print(tools_prompt)