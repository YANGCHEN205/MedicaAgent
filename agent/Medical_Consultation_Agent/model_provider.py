# import os, json
# import dashscope
# from agent.Medical_Knowledgebase_Agent.prompt import user_prompt
# from dashscope.api_entities.dashscope_response import Message
# from transformers import AutoModelForCausalLM, AutoTokenizer,RobertaTokenizer, RobertaModel
# import torch



# class ModelProvider(object):
#     def __init__(self):
#         # 设置最大重试次数
#         self.device = "cuda"
#         self.max_retry_time = 1
#         self.local_run = True
#         if self.local_run:
#             # 从环境变量中获取API密钥和模型名称
#             self.api_key = "sk-dd3b645e78c24ebbbfc34971555c05fa"
#             self.model_name = "qwen-max"
#             # 初始化dashscope客户端
#             self._client = dashscope.Generation()
#         else:
#             # "Qwen/Qwen1.5-0.5B-chat" "Qwen/Qwen2-7B-Instruct"
#             self.model_name = "Qwen/Qwen2-7B-Instruct"
#             self.cache_dir = "/root/autodl-tmp/hug/"
#             self.model = AutoModelForCausalLM.from_pretrained(
#                 self.model_name,
#                 torch_dtype=torch.bfloat16,
#                 trust_remote_code=True,
#                 cache_dir=self.cache_dir
#             ).to(self.device)
#             self.tokenizer = AutoTokenizer.from_pretrained(
#                 self.model_name, trust_remote_code=True, cache_dir=self.cache_dir)

        
#     def chat(self, system_prompt, chat_history):
#         cur_retry_time = 0
#         while cur_retry_time < self.max_retry_time:
#             cur_retry_time += 1
#             if self.local_run:
#                 try:
#                     # 构建消息列表，包括系统提示、用户提示和历史聊天记录
#                     # messages = [
#                     #     Message(role="system", content=system_prompt),
#                     #     Message(role="user", content=user_prompt)
#                     # ]
#                     # for his in chat_history:
#                     #     messages.append(Message(role="user", content=his[0]))
#                     #     messages.append(Message(role="assistant", content=his[1]))
#                     messages = []
#                     for his in chat_history:
#                         messages.append(Message(role="user", content=his[0]))
#                         messages.append(Message(role="assistant", content=his[1]))
#                     # 构建消息列表，包括系统提示、用户提示和历史聊天记录
#                     messages.append(Message(role="system", content=system_prompt))
#                     messages.append(Message(role="user", content=user_prompt))
#                     # 调用模型API并获取响应
#                     response = self._client.call(
#                         model=self.model_name,
#                         api_key=self.api_key,
#                         messages=messages,
#                         # result_format='message',  # set the result to be "message"  format.
#                         # stream=True, # set streaming output
#                         # incremental_output=True  # get streaming output incrementally
#                         )
#                     # print(response)
#                     # 解析模型响应并返回内容
#                     content = self._parse_model_response(response)
#                     return content
#                 except Exception as e:
#                     print(f"call llm exception: {e}")
#             else:
#                 try:
#                     messages = [
#                         {"role": "system", "content": system_prompt},
#                         {"role": "user", "content": user_prompt}
#                         ]
#                     for his in chat_history:
#                         messages.append({"role": "user", "content": his[0]})
#                         messages.append({"role": "assistant", "content": his[1]})
#                     text = self.tokenizer.apply_chat_template(
#                         messages,
#                         tokenize=False,
#                         add_generation_prompt=True
#                     )
#                     model_inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
#                     generated_ids = self.model.generate(
#                         model_inputs.input_ids,
#                         max_new_tokens=512
#                     )
#                     generated_ids = [
#                         output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
#                     ]

#                     response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
#                     # print(response)
#                     # 解析模型响应并返回内容
#                     content = self._parse_model_response(response)
#                     return content
#                 except Exception as e:
#                     print(f"call llm exception: {e}")        
#         return {}

#     def _parse_model_response(self, response):
#         """尝试解析模型响应为JSON格式"""
#         text = response["output"]["text"] if self.local_run else response
#         try:
#             # 尝试直接解析文本为JSON
#             return json.loads(text)
#         except json.JSONDecodeError:
#             # 如果直接解析失败，尝试查找被标记的JSON字符串
#             json_start = text.find("```json")
#             json_end = text.rfind("```")
#             json_content = text[json_start + 7:json_end]
#             return json.loads(json_content)
