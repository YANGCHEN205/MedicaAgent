import os
import sys
sys.path.append(os.path.abspath('.'))
import json
from datetime import datetime
from agent.Idle_Chat_Agent.main import Idle_Chat_Agent
from agent.Medical_Appointment_Agent.main import Medical_Appointment_Agent
from agent.Medical_Consultation_Agent.main import Medical_Consultation_Agent
from agent.Medical_Knowledgebase_Agent.main import Medical_Knowledgebase_Agent
mka_agent = Medical_Knowledgebase_Agent()
maa_agent = Medical_Appointment_Agent()
mca_agent = Medical_Consultation_Agent()
ica_agent = Idle_Chat_Agent()


def query_user_for_details(prompt):
    return prompt

def finish(answer):
    """ 结束对话并给出最终答案 """
    return answer

def idle_chat_agent(query_agent):
    # 闲聊Agent
    result = ica_agent.agent_execute(query_agent, max_request_time=3,debug=True)
    # result =  "用户的闲聊任务已经执行成功，返回了用户的需求，请执行下一步。用户的闲聊任务已经执行成功，返回了用户的需求，请执行下一步。用户的闲聊任务已经执行成功，返回了用户的需求，请执行下一步。"
    return result
def medical_appointment_agent(query_agent):
    # 医疗预约agent
    result = maa_agent.agent_execute(query_agent, max_request_time=6,debug=True)
    # result +=  """医疗预约已经执行成功，此消息确认您的预约请求已成功处理。返回了用户的需求"""
    return result
def medical_consultation_agent(query_agent):
    # 医疗智能问诊Agent
    result = mca_agent.agent_execute(query_agent, max_request_time=6,debug=True)
    # result =  "智能医疗问诊已经执行成功，返回了用户的需求"
    return result
def  medical_knowledgebase_agent(query_agent):
    # 医疗知识库Agent
    result = mka_agent.agent_execute(query_agent, max_request_time=6,debug=True)
    # result =  "智能医疗库知识已经执行成功，返回了用户的需求"
    return result



tools_info = [
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
                        "description": "通常为对用户问题的回答或解决方案。"
                    }
                }
            },
            "required": ["answer"]
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_user_for_details",
            "description": "向用户提问，询问用户是否满意和是否有别的需求，满意后调用finish结束对话。",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "向用户提问，询问用户是否满意和是否有别的需求，满意后调用finish结束对话"
                    }
                },
            },
            "required": ["prompt"]
        }
    },
    {
        "type": "function",
        "function": {
            "name": "idle_chat_agent",
            "description": "闲聊Agent。执行与用户的非正式闲聊。闲聊，用户的非医学方面和非预约的需求",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_agent": {
                        "type": "string",
                        "description": "用户提供的非医学和闲聊需求，一般为用户的直接输入语言，用于引导闲聊的方向。"
                    }
                },
            },
            "required": ["query_agent"]
        }
    },
    {
        "type": "function",
        "function": {
            "name": "medical_appointment_agent",
            "description": "医疗预约agent。处理用户的医疗预约请求。执行预约，查询医院医生值日情况，返回医生预约情况",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_agent": {
                        "type": "string",
                        "description": "用户的预约要求需求，一般为用户的直接输入语言，用于详细了解预约的需求。"
                    }
                },
            },
            "required": ["query_agent"]
        }
    },
    {
        "type": "function",
        "function": {
            "name": "medical_consultation_agent",
            "description": "智能医疗问诊Agent。完成用户需要问诊的需求。执行医疗问诊，为用户提供医疗咨询，询问用户的病症，生成诊断结果。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_agent": {
                        "type": "string",
                        "description": "用户的普通的问诊需求，一般为用户的直接输入语言，用于详细了解医疗咨询的需求。"
                    }
                },
            },
            "required": ["query_agent"]
        }
    },
    {
        "type": "function",
        "function": {
            "name": "medical_knowledgebase_agent",
            "description": "智能医疗库知识库agent。提供医疗知识库的访问，支持用户查找特定的医疗信息。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_agent": {
                        "type": "string",
                        "description": "用户的普通医疗知识的需求输入，一般为用户的直接输入语言，用于指导搜索医疗知识库的具体内容。"
                    }
                },
            },
            "required": ["query_agent"]
        }
    }
]


# 工具使用逻辑说明
action_logic = "调用finish结束对话之前。向用户提问，询问用户是否满意和是否有别的需求，满意后调用finish结束对话"
# """
# 1. 如果用户询问的是直接的医疗相关的知识，包括医学常识等，直接调用医疗知识库medical_knowledgebase_agent。
# 2. 如果用户询问的是非医学相关的需求，比如日常闲聊，直接调用闲聊助手idle_chat_agent。
# 3. 如果用户想要医疗问诊，需求医疗的诊断，直接调用medical_consultation_agent。
# 4. 如果用户想要预约医生，查询医生的信息，直接调用medical_appointment_agent。
# """
# 工具映射逻辑

tools_map = {
    "query_user_for_details": query_user_for_details,
    "finish": finish,
    "idle_chat_agent": idle_chat_agent,
    "medical_appointment_agent": medical_appointment_agent,
    "medical_consultation_agent": medical_consultation_agent,
    "medical_knowledgebase_agent": medical_knowledgebase_agent
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



