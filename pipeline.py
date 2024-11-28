from latex import Latex
from consts import *
from models import Model
import streamlit as st
from time import time
from datetime import datetime
from utils import free_gpu

file_dir = "latex_codes.txt"
textboxs = []

def on_button_click():
    st.session_state.count += 1

def summarize(model, texts, verbose = False):
    summary =  ""
    start = time()
    for text in texts:
        summary += model.call_model(
            prompt = summary_prompt,
            text = text,
            max_token = 300
        )
    finish = time()
    token_sec = model.get_tks(summary, finish-start)
    if verbose:
        print(summary)
        print(token_sec)
        print("token/second")
    return summary, token_sec


def merge(model, sums, verbose = False)->str:
    sums = model.call_model(
        prompt = merge_prompt_other,
        text = sums,
        max_token = 300
    )

    if verbose: print(sums)

    return sums


def convert_to_latex(model, summary, filename, verbose = False) :
    latex_code = model.call_model(latex_prompt_other, summary, 600)
    if verbose: print(latex_code)

    code = latex_code.split("```")
    if(len(code) == 3):
        latex_code = code[1]

    print("=================")
    print(latex_code)
    print("+++++++++++++++++")

    latex = Latex(latex_code, filename)

    compile_result = latex.compile()
    return compile_result,latex_code

def refine_latex(model,previous_latex_code,compile_result,filename, verbose = False):
    refined_result = "err"
    cutoff = 5
    if compile_result =="pdf is created": 
        return compile_result,previous_latex_code
    else:
        prompt = refine_prompt.format(previous_latex_code,compile_result) 
        while not refined_result=="pdf is created" and cutoff>0:
            cutoff-=1
            refined_code = model.call_model(prompt,"give me ONLY the correct latex code:",1000 )
            
            if verbose: print(refined_code)

            latex = Latex(refined_code, filename)

            refined_result = latex.compile() 
    return refined_result,refined_code


def main():
    filename = f"out_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}"
    st.title("Latex Code Generator of Multiple Scientific Texts")

    verbose = False
    if(st.checkbox("Verbose")):
        verbose = True

    model_name = st.selectbox(
        "Model",
        ("HuggingFaceTB/SmolLM2-1.7B-Instruct", "openbmb/MiniCPM-2B-dpo-bf16", "Qwen/Qwen2.5-1.5B-Instruct", "gpt")
    )
    model = Model(model_name)

    if "count" not in st.session_state:
        st.session_state.count = 0

    if st.button("Add New Text Box"):
        on_button_click()

    for i in range(st.session_state.count):
        text = st.text_area("Place Your Text Here!", height = 200, key = f"textarea_{i}")
        textboxs.append(text)

    if st.button("Generate PDFs"):
        texts = [text for text in textboxs if text]
        if texts:
            with st.spinner("Generating Summaries..."):
                sums, token_per_second = summarize(model, texts, verbose)
            st.markdown(f"**Token/Second: {token_per_second}**")
            
            with st.spinner("Merging Summaries..."):
                merged_summary = merge(model, sums, verbose)
            
            with st.spinner("Converting to LaTeX..."):
                compile_result, latex_code = convert_to_latex(model, merged_summary, filename, verbose)                
                refined_result, refined_latex_code = refine_latex(
                    model = model,
                    previous_latex_code = latex_code,
                    compile_result = compile_result,
                    filename = filename,
                    verbose = verbose
                )
                with open(file_dir, 'w+') as f :
                    f.write(refined_latex_code)
                    f.write('*SSS*')

            if refined_result == compile_result or refined_result == "pdf is created":
                free_gpu(model)
                try:
                    with open(f"./outputs/{filename}.pdf", mode = "rb") as f:
                        st.download_button(f"Download PDF", f, file_name = f"{filename}.pdf")
                    with open(f"./outputs/{filename}.tex", mode = "rb") as f:
                        st.download_button(f"Download LaTeX Code", f, file_name = f"{filename}.tex")
                except FileNotFoundError:
                    st.warning(f"Couldn't create pdf after 5 attempt...")
                else:
                    st.success(f"PDF generated successfully!")
            else:
                st.warning(f"Couldn't create pdf after 5 attempt...")
        else:
            st.warning(f"No input. Skipping...")



if __name__ == "__main__":
    main()
