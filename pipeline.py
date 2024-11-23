from latex import Latex
from consts import *
from gpt import call_chatgpt
from models import Model
#1 getting text/s
verbose = True
model = Model("gpt")
def get_text()->str:
    pass


#2 summarize
def summarize(texts):
    summary= ""
    for text in texts:

        summary += model.call_model(
            prompt = summary_prompt,
            text = text,
            max_token= 300
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

    latex_code = model.call_model(latex_prompt,summary,600)
    if verbose: print(latex_code)

    latex = Latex(latex_code,"3")

    print(latex.compile())

if __name__=="__main__":
    convert_to_latex(merge(summarize([papers])))