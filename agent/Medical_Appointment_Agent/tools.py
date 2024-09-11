import json
import os
import sys
sys.path.append(os.path.abspath('.'))
from datetime import datetime
from agent.Medical_Appointment_Agent.hospital_data import hospital_data
import sys
import os
from typing import Dict, List, Union, Optional
def _get_workdir_root():
    workdir_root = os.environ.get('WORKDIR_ROOT', "./data/travel_history")
    return workdir_root
WORKDIR_ROOT = _get_workdir_root()
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

# 查询特定科室的所有医生信息
def query_doctors_by_department(department):
    if department in hospital_data:
        return hospital_data[department]
    return f"没有找到{department}科室的信息。"

# # 模拟预约函数
# def book_appointment(patient_name, department, doctor_name, appointment_date):
#     """## _summary_

#     ### Args:
#         - `patient_name (_type_)`:患者姓名
#         - `department (_type_)`: 要预约的科室名称
#         - `doctor_name (_type_)`: 要预约的医生姓名
#         - `appointment_date (_type_)`: 出诊的时间
#     ### Returns:
#         - `_type_`: _description_
#     """
#     # 将日期字符串转换为 datetime 对象
#     # appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d")
#     # 查找科室和医生
#     if department not in hospital_data:
#         return f"科室 {department} 不存在。"
    
#     doctors = hospital_data[department]
#     selected_doctor = None
    
#     for doctor in doctors:
#         if doctor["姓名"] == doctor_name:
#             selected_doctor = doctor
#             break
    
#     if not selected_doctor:
#         return f"医生 {doctor_name} 不在 {department} 科室。"
    
#     # 模拟预约成功，返回预约信息
#     appointment_info = {
#         "患者姓名": patient_name,
#         "预约科室": department,
#         "预约医生": doctor_name,
#         # "预约日期": appointment_date.strftime("%Y年%m月%d日"),
#         "医生职称": selected_doctor["职称"],
#         "医生专长": selected_doctor["专长"],
#         "出诊时间": selected_doctor["出诊时间"]
#     }
    
#     return appointment_info




# 假设 hospital_data 已经填充了具体的科室和医生数据

def book_appointment(patient_name: str, department: str, doctor_name: str, appointment_date: str) -> Dict[str, Union[str, int]]:
    """模拟预约医生。

    Args:
        patient_name (str): 患者姓名
        department (str): 要预约的科室名称
        doctor_name (str): 要预约的医生姓名
        appointment_date (str): 预约日期

    Returns:
        Dict[str, Union[str, int]]: 预约信息或错误信息
    """
    doctors = query_doctors_by_department(department)
    if isinstance(doctors, str):
        return {"错误": doctors}
    
    selected_doctor: Optional[Dict[str, Union[str, int]]] = next((doc for doc in doctors if doc["姓名"] == doctor_name), None)
    
    if not selected_doctor:
        return {"错误": f"医生 {doctor_name} 不在 {department} 科室。"}
    
    # try:
    #     formatted_date =  datetime.strptime(appointment_date, "%Y-%m-%d")
    # except ValueError:
    #     return {"错误": "无效的日期格式。正确格式应为YYYY-MM-DD。"}
    appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d")
    appointment_info = {
        "患者姓名": patient_name,
        "预约科室": department,
        "预约医生": doctor_name,
        "预约日期": appointment_date.strftime("%Y年%m月%d日"),
        "医生职称": selected_doctor["职称"],
        "医生专长": selected_doctor["专长"],
        "出诊时间": selected_doctor["出诊时间"],
        "医生教育背景": selected_doctor.get("教育背景", "未提供"),
        "医生工作经验": f"{selected_doctor.get('工作经验', '未提供')}"
    }
    
    return appointment_info


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
            "description": "结束对话并给出最终预约的详细信息。",
            "parameters": {
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "dict",
                        "description": "包含最预约的字典，输出为完整的答案。"
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
            "parameters": {},  
            "required": []
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_doctors_by_department",
            "description": "查询特定科室的医生信息。",
            "parameters": {
                "type": "object",
                "properties": {
                    "department": {
                        "type": "string",
                        "description": "要查询的科室名称。"
                    }
                }
            },
            "required": ["department"]
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "为患者预约特定科室医生的时间。",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_name": {
                        "type": "string",
                        "description": "患者的姓名。"
                    },
                    "department": {
                        "type": "string",
                        "description": "要预约的科室名称。"
                    },
                    "doctor_name": {
                        "type": "string",
                        "description": "要预约的医生姓名。"
                    },
                    "appointment_date": {
                        "type": "string",
                        "description": "预约日期，格式为YYYY-MM-DD。"
                    }
                }
            },
            "required": ["patient_name", "department", "doctor_name", "appointment_date"]
        }
    }
]

# 工具使用逻辑说明
action_logic = """
1.使用工具 'book_appointment' 前，需先调用 'get_current_date' 获取当前日期。'get_current_date' 返回的日期将作为 'book_appointment' 中 'appointment_date' 参数的值，用于确保预约操作使用当前日期进行处理。
2. 你有任何不清楚的信息，使用query_user_for_details向用户提问。
"""
# 工具映射逻辑
tools_map = {
    "query_user_for_details": query_user_for_details,
    "finish":finish,
    "book_appointment":book_appointment,
    "get_current_date":get_current_date,
    "query_doctors_by_department":query_doctors_by_department
}
import json

import json

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



# # 示例调用
# department_name = "外科"
# doctor_name = "张飞"
# patient_name = "李四"
# appointment_date = datetime(2024, 9, 10)

# appointment_info = book_appointment(patient_name, department_name, doctor_name, appointment_date)
# print(appointment_info)
