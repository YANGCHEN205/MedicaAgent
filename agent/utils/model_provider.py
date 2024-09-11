import os
import sys
sys.path.append(os.path.abspath('.'))
import re
import json
import yaml
import torch
import dashscope
from dashscope.api_entities.dashscope_response import Message
from transformers import AutoModelForCausalLM, AutoTokenizer

class ModelProvider(object):
    def __init__(self):
        self.config = self.load_config('./agent/utils/config.yaml')
        self.initialize_model()

    def load_config(self, config_path):
        with open(config_path, 'r') as config_file:
            return yaml.safe_load(config_file)

    def initialize_model(self):
        self.device = self.config['device']
        self.max_retry_time = self.config['max_retry_time']
        self.nolocal_run = self.config['nolocal_run']
        
        if self.nolocal_run:
            self.api_key = self.config['api_key']
            self.model_name = self.config['local_model_name']
            self._client = dashscope.Generation()
        else:
            self.model_name = self.config['remote_model_name']
            self.cache_dir = self.config['cache_dir']
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.bfloat16,
                trust_remote_code=True,
                cache_dir=self.cache_dir
            ).to(self.device)
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name, trust_remote_code=True, cache_dir=self.cache_dir)
        
    def chat(self, system_prompt, user_prompt, chat_history):
        try:
            return self.attempt_chat(system_prompt, user_prompt, chat_history)
        except Exception as e:
            print(f"Model call exception: {e}")
            return {}

    def attempt_chat(self, system_prompt, user_prompt, chat_history):
        messages = self.build_messages(system_prompt, user_prompt, chat_history)
        if self.nolocal_run:
            return self.local_model_call(messages)
        else:
            return self.remote_model_call(messages)

    def build_messages(self, system_prompt, user_prompt, chat_history):
        if self.nolocal_run:

            messages = []
            for his in chat_history:
                messages.append(Message(role="user", content=his[0]))
                messages.append(Message(role="assistant", content=his[1]))
            # 构建消息列表，包括系统提示、用户提示和历史聊天记录
            messages.append(Message(role="system", content=system_prompt))
            messages.append(Message(role="user", content=user_prompt))
        else:
            messages = []
            for his in chat_history:
                messages.append({"role": "user", "content": his[0]})
                messages.append({"role": "assistant", "content": his[1]})
            messages.append([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
                ])
        return messages

    def local_model_call(self, messages):
        response = self._client.call(
            model=self.model_name,
            api_key=self.api_key,
            messages=messages)
        return self._parse_model_response(response)

    def remote_model_call(self, messages):
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
        generated_ids = self.model.generate(model_inputs.input_ids, max_new_tokens=512)
        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return self._parse_model_response(response)

    def _parse_model_response(self, response):
        try:
            return json.loads(self.remove_json_comments(response["output"]["text"]) if self.nolocal_run else response)
        except json.JSONDecodeError:
            json_start = response.find("```json")
            json_end = response.rfind("```")
            json_content = response[json_start + 7:json_end]
            return json.loads(json_content)


    def remove_json_comments(self,json_str):
        # Remove single-line comments
        json_str = re.sub(r"//.*", "", json_str)
        # Remove multi-line comments
        json_str = re.sub(r"/\*.*?\*/", "", json_str, flags=re.DOTALL)
        return json_str


