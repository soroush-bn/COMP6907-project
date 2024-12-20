# LLMs stored in ~/.cache/huggingface

from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel
from consts import *
import torch, requests
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

'''
Models:
1. HuggingFaceTB/SmolLM2-1.7B-Instruct
2. openbmb/MiniCPM-2B-dpo-bf16
3. Qwen/Qwen2.5-1.5B-Instruct
'''

class Model():
    def __init__(self, model_name) -> None:
        self.model_name = model_name
        self.load_in_4bit = False
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.embedding_model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    def eval(self, model_names, latex_codes):
        eval_result = []
        for model,latex in zip(model_names,latex_codes):
            eval_result.append(self.call_model(evaluation_prompt, f"{model}:{latex}", 600))
        return eval_result
    
    def __embed_text(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            embeddings = self.embedding_model(**inputs).last_hidden_state
        return embeddings.mean(dim=1)
    
    def get_similarity(self, latex_codes):
        embeddings = np.array([np.squeeze(self.__embed_text(code).numpy()) for code in latex_codes])
        print(embeddings.shape)
        similarity_matrix = cosine_similarity(embeddings)
        return similarity_matrix

    def __number_of_tokens(self, text):
        return len(self.tokenizer.tokenize(text))
    
    def get_tks(self, text, time):
        return self.__number_of_tokens(text)/time
     
    def call_model(self, prompt, text, max_token):
        if self.model_name != "gpt" :
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model = AutoModelForCausalLM.from_pretrained(self.model_name, trust_remote_code = True, load_in_4bit=self.load_in_4bit).to("cuda")

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
            return out.split("<|im_start|>")[3].split("\n", 1)[1].replace("<|im_end|>", "").strip()
        else:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "gpt-3.5-turbo" if self.model_name=="gpt" else "gpt-4o-mini",  # Use "gpt-3.5-turbo" for the GPT-3.5 model
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
