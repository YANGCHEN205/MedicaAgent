import os
import sys
sys.path.append(os.path.abspath('.'))
from agent.Central_Control_Agent.tools import gen_tools_desc,tools_map, query_user_for_details
# 医疗助手的任务描述与限制
constraints = [
    "你仅使用以下下面列出的动作，你不能直接回答用户的问题，只能分配以下功能。",
    "你只能分配功能。"
]


resources = [
    "你只可以使用以上的相应的专业工具模块，不需要别的知识",
]



# 策略部分简化，减少复杂性
strategies = [
    "确认用户的需求，你只能调度以下相应的专业工具和询问用户需求。",
    "如果用户的需求涉及多个方面，每次只处理一个需求，确保对话流程简洁有序。",
    "根据上一步的结果，自主推理下一步"
    "确保信息简洁准确，快速为用户提供最合适的回答，避免冗余信息。"
    ]



# 模板填充
prompt_template = """
    您现在是控制中心助手，负责处理用户提交的各类问题，并根据问题的性质指派以下工具进行处理。
    你只能调用以下query_user_for_details,finish,idle_chat_agent,medical_appointment_agent,medical_consultation_agent,medical_knowledgebase_agent工具，自己完全不能回答用户的需求。
    在处理完成后，您还需要接收其反馈，并基于这些反馈确定是否需要进一步的操作或可以调用finfish结束对话。
    目标或其他条件:
    {query}
    限制条件说明:
    {constraints}
    动作说明: 你只能有的调用以下有的工具，不能调用不存在的工具。请严格按照以下的工具执行，你只能调用以下的几个工具包。首先根据用户的问题匹配合适的工具。如果问题涉及多个方面，确保逐一解决。
    {actions}
    资源说明:
    {resources}
    策略说明:
    {strategies}
    上一步执行的动作及结果如下：
    history: {agent_scratch}
    请严格按照以下的 JSON 格式进行响应，响应格式如下:
    {response_format_prompt}
"""


# 修改后的 JSON 格式响应
response_format_prompt = """
{
    "action": {
        "name": "动作名称",
        ## 不能返回该动作不存在的参数
        "parameters": {
            "parameters name": "执行动作所需参数的值"
        }
    },
    "thoughts": {
        "planning": "解决用户问题的具体实现步骤",
        "reflection": "建设性的自我批评与反思",
        "summary": "当前步骤的总结，提供给用户的反馈",
        "history": "上一步的动作及结果回顾"
        "reasoning": "进行推理下一步动作。读取动作反馈的结果，推理。不能调用不存在的工具。"
    },
    "observation": "观察当前任务的整体进度"
}
"""

# 生成动作说明描述
action_prompt = gen_tools_desc()
# 将限制条件、资源和策略等内容进行拼接，以便在模板中使用
constraints_prompt = "\n".join([f"{idx+1}.{con}" for idx, con in enumerate(constraints)])
resources_prompt = "\n".join([f"{idx+1}.{con}" for idx, con in enumerate(resources)])
strategies_prompt = "\n".join([f"{idx+1}.{con}" for idx, con in enumerate(strategies)])

# 生成最终的提示信息
def gen_prompt(query, agent_scratch):
    prompt = prompt_template.format(
        query=query,
        constraints=constraints_prompt,
        actions=action_prompt,
        resources=resources_prompt,
        strategies=strategies_prompt,
        agent_scratch=agent_scratch,
        response_format_prompt=response_format_prompt
    )
    return prompt


user_prompt = """
您现在是控制中心助手，负责处理用户提交的各类问题，并根据问题的性质和意图指以下相应的专业工具进行处理。
在以下相应的专业工具处理完成后，您还需要接收其反馈，并基于这些反馈确定是否需要进一步的操作或使用finish可以结束对话。
请确保您的回应精准并满足用户的需求，请严格按照以下的JSON格式进行响应：
"""

