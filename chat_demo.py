import os
import sys
sys.path.append(os.path.abspath('.'))







from agent.Central_Control_Agent.main import Central_Control_Agent
if __name__ == "__main__":
    agent = Central_Control_Agent()
    while True:
        try:
            sys.stdout.write("请输入你的需求:")
            sys.stdout.flush()  # 确保提示信息被打印出来
            user_input = sys.stdin.readline().strip().encode('utf-8').decode('utf-8', errors='ignore')
            if user_input.lower() == 'exit':
                break

            response = agent.agent_execute(user_input, max_request_time=5,debug=True)
            print("系统：", response)
        except UnicodeDecodeError as e:
            print(f"输入处理错误: {e}")
            

# python /root/autodl-tmp/MedicaAgent/chat_demo.py | tee /root/autodl-tmp/MedicaAgent/log/ica.log