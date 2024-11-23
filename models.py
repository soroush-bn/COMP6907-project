# LLMs stored in ~/.cache/huggingface
import os 
import sys
sys.path.append(r"E:\programming\anaconda3\envs\cuda\lib\site-packages")
import transformers 
# from transformers import AutoModelForCausalLM, AutoTokenizer
from consts import *
import torch

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)
print(transformers)
'''
Models:
1. HuggingFaceTB/SmolLM2-1.7B-Instruct
2. openbmb/MiniCPM-2B-dpo-bf16
3. Qwen/Qwen2.5-1.5B-Instruct
'''
class Model():
    def __init__(self) -> None:
        self.model_name = "gpt"
        self.max_token = 500
        self.prompt = ""
        self.text= ""
        
    def call_model(self,modelName, prompt, text, maxToken):
        device = "cuda"
        tokenizer = transformers.AutoTokenizer.from_pretrained(modelName)
        model = transformers.AutoModelForCausalLM.from_pretrained(modelName, trust_remote_code = True,low_cpu_mem_usage=True).to(device)

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
        inputs = tokenizer.encode(input_text, return_tensors = "pt").to(device)
        outputs = model.generate(
            inputs,
            max_new_tokens = maxToken,
            temperature = 0.7,
            top_p = 0.9,
            do_sample = True
        )
        out = tokenizer.decode(outputs[0])
        if(modelName == "HuggingFaceTB/SmolLM2-1.7B-Instruct"):
            return out.split("<|im_start|>assistant")[1].replace("<|im_end|>", "").strip()
        elif(modelName == "openbmb/MiniCPM-2B-dpo-bf16"):
            return out.split("<AI>")[1].replace("</s>", "").strip()
        return out.split("<|im_start|>system")[2].replace("<|im_end|>", "").strip()
