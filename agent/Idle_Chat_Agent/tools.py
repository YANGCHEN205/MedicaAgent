import os
import sys
sys.path.append(os.path.abspath('.'))
import json
from datetime import datetime




def query_user_for_details(prompt):
    return prompt

def finish(answer):
    """ 结束对话并给出最终答案 """
    return answer

def get_current_date():
    # 获取当前日期，并将其格式化为字符串 'YYYY-MM-DD'
    current_date_str = datetime.now().strftime("%Y-%m-%d %A")
    
    # 映射英文星期到中文
    week_day_map = {
        'Monday': '周一',
        'Tuesday': '周二',
        'Wednesday': '周三',
        'Thursday': '周四',
        'Friday': '周五',
        'Saturday': '周六',
        'Sunday': '周日'
    }
    
    # 分割日期字符串以获取英文星期名称
    date_part, week_day_en = current_date_str.split()
    
    # 获取中文星期名称
    week_day_cn = week_day_map[week_day_en]
    
    # 生成最终的日期字符串，包括中文的星期
    current_date_result = f"现在日期是：{date_part} {week_day_cn}"
    return current_date_result


tools_info = [
    {
        "type": "function",
        "function": {
            "name": "query_user_for_details",
            "description": "向用户提问，用于获取更多信息，以深入了解用户的需求。",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "用户输入的信息，用于明确用户的需求。"
                    }
                },
            },
            "required": ["prompt"]
        }
    },
    {
        "type": "function",
        "function": {
            "name": "finish",
            "description": "结束对话并给出最终用户此轮对话的结果。",
            "parameters": {
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "dict",
                        "description": "最终用户此轮对话的结果。"
                    }
                }
            },
            "required": ["answer"]
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_date",
            "description": "获取当前日期并以字符串格式返回。",
            "parameters": {},  # 无需参数
            "required": []
        }
    }
]

# 工具使用逻辑说明
action_logic = """
1. 你有任何不清楚的信息，使用query_user_for_details向用户提问。
"""
# 工具映射逻辑
tools_map = {
    "query_user_for_details": query_user_for_details,
    "finish":finish,
    "get_current_date":get_current_date
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



