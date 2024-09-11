import sys
import os
sys.path.append(os.path.abspath('.'))
from agent.utils.model_provider import ModelProvider
from agent.Medical_Knowledgebase_Agent.prompt import query_user_for_details,gen_prompt, user_prompt,tools_map
from dotenv import load_dotenv
import dashscope
import os
import json

load_dotenv()

class Medical_Knowledgebase_Agent(object):
    def __init__(self):
        self.mp = ModelProvider()
        dashscope.api_key = "sk-f529539e3a50472fac783cf1e99fddef"
        os.environ["TAVILY_API_KEY"] = "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"

    def parse_thoughts(self, response, cur_request_time, max_request_time, debug):
        try:
            thoughts = response.get("thoughts")
            planning = thoughts.get("planning")
            reasoning = thoughts.get("reasoning")
            reflection = thoughts.get("reflection")
            history = thoughts.get("history")
            summary = thoughts.get("summary")
            observation = response.get("observation")
            prompt = f"planning: {planning}\nreasoning: {reasoning}\nreflection: {reflection}\nhistory: {history}\nobservation: {observation}\nsummary: {summary}"
            return prompt
        except Exception as e:
            print(f"parse_thoughts error: {e}")
            return ""

    def execute_action(self, action_name, action_args, debug):
        try:
            func = tools_map.get(action_name)
            result = func(**action_args)
            if debug:
                print(f"action_name: {action_name}, action_args: {action_args}")
            return result
        except Exception as e:
            print(f"调用工具异常： {e}")
            return str(e)

    def agent_execute(self, query, max_request_time=5, debug=False):
        cur_request_time = 0
        chat_history = []
        agent_scratch = ""

        while cur_request_time < max_request_time:
            cur_request_time += 1
            prompt = gen_prompt(query, agent_scratch)
            response = self.mp.chat(prompt,user_prompt,chat_history)

            if not response or not isinstance(response, dict):
                print(f"call llm exception, response is: {response}")
                continue

            action_info = response.get("action")
            action_name = action_info.get("name")
            action_args = action_info.get("parameters")
            if debug:
                print(f'-------------医学知识库Agent第{cur_request_time}次推断------------')
                print(json.dumps(response, ensure_ascii=False, indent=4))

            if action_name == "query_user_for_details":
                user_response = input(query_user_for_details(action_args["prompt"]))
                chat_history.append([action_args["prompt"], user_response])
                agent_scratch += f"query_user: {action_args['prompt']}user response: {user_response}"
                continue

            call_function_result = self.execute_action(action_name, action_args, debug)
            agent_scratch += f"observation: {response.get('observation')} execute action {action_name} result: {call_function_result}"
            assistant_msg = self.parse_thoughts(response, cur_request_time, max_request_time, debug)
            chat_history.append([user_prompt, assistant_msg])

            if action_name == "finish":
                final_answer = action_args.get("answer")
                break

        if cur_request_time == max_request_time:
            final_answer = "本次任务执行失败！未能提供相关医疗知识"
        print(f"final_answer: {final_answer}")
        return final_answer


if __name__ == "__main__":
    mka_agent = Medical_Knowledgebase_Agent()
    max_request_time = 6
    query = '你好，腱鞘炎应该吃什么'
    final_answer = mka_agent.agent_execute(query, max_request_time=max_request_time,debug=True)
    # print(f"final_answer: {final_answer}")