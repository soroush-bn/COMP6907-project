from latex import Latex
from consts import *
from gpt import call_chatgpt
from models import Model
#1 getting text/s
verbose = True
def get_text()->str:
    pass


#2 summarize
def summarize(texts):
    summary= ""
    model = Model()
    for text in texts:

        summary += model.call_model(
            modelName = "Qwen/Qwen2.5-1.5B-Instruct",
            prompt = summary_prompt_other,
            text = text,
            maxToken = 300
        )
        # summary+=(call_chatgpt(summary_prompt+text,300,API_KEY))
    if verbose: print(summary)
    return summary


#3 merge
def merge(sums)->str:
    if verbose: print(sums)

    return sums


# latex
def convert_to_latex(summary) :

    latex_code = call_chatgpt(latex_prompt+summary,600,API_KEY)
    if verbose: print(latex_code)

    latex = Latex(latex_code)

    print(latex.compile())

if __name__=="__main__":
    convert_to_latex(merge(summarize([papers])))