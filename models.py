# LLMs stored in ~/.cache/huggingface
# import os 
# import sys
# sys.path.append(r"E:\programming\anaconda3\envs\cuda\lib\site-packages")
import transformers 
# from transformers import AutoModelForCausalLM, AutoTokenizer
from consts import *
import requests

'''
Models:
1. HuggingFaceTB/SmolLM2-1.7B-Instruct
2. openbmb/MiniCPM-2B-dpo-bf16
3. Qwen/Qwen2.5-1.5B-Instruct

'''
class Model():
    def __init__(self, model_name) -> None:
        self.model_name = model_name
        # self.max_token = 500
        self.prompt = ""
        self.text = ""
        self.tokenizer = transformers.AutoTokenizer.from_pretrained('bert-base-uncased')


    def __number_of_tokens(self, text):
        tokens = self.tokenizer.tokenize(text)
        return len(tokens)
    def get_tks(self,text,time):
        return self.__number_of_tokens(text)/time 
    def call_model(self, prompt, text, max_token):
        if self.model_name != "gpt" :
            tokenizer = transformers.AutoTokenizer.from_pretrained(self.model_name)
            model = transformers.AutoModelForCausalLM.from_pretrained(self.model_name, trust_remote_code = True).to("cuda")

            messages = [
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
            
            input_text = tokenizer.apply_chat_template(messages, tokenize = False)
            inputs = tokenizer.encode(input_text, return_tensors = "pt").to("cuda")
            outputs = model.generate(
                inputs,
                max_new_tokens = max_token,
                temperature = 0.7,
                top_p = 0.9,
                do_sample = True
            )
            out = tokenizer.decode(outputs[0])
            if(self.model_name == "HuggingFaceTB/SmolLM2-1.7B-Instruct"):
                return out.split("<|im_start|>assistant")[1].replace("<|im_end|>", "").strip()
            elif(self.model_name == "openbmb/MiniCPM-2B-dpo-bf16"):
                return out.split("<AI>")[1].replace("</s>", "").strip()
            return out.split("<|im_start|>system")[2].replace("<|im_end|>", "").strip()
        else:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "gpt-3.5-turbo",  # Use "gpt-3.5-turbo" for the GPT-3.5 model
                "messages": [{"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": prompt+text}],
                "temperature": 0.7,  # Adjust for creativity (0.0 for deterministic, 1.0 for creative)
                "max_tokens": max_token  # Adjust for desired response length
            }

            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                raise Exception(f"Error: {response.status_code} - {response.text}")
