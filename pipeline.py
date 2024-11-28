from latex import Latex
from consts import *
from models import Model
import streamlit as st


verbose = True

def get_text():
    text1 = st.text_area("Text 1", height=200)
    text2 = st.text_area("Text 2", height=200)
    text3 = st.text_area("Text 3", height=200)

    return [text1, text2, text3]

#2 summarize
def summarize(model, texts):
    summary =  ""
    for text in texts:
        summary += model.call_model(
            prompt = summary_prompt,
            text = text,
            max_token = 300
        )
    if verbose: print(summary)
    return summary


#3 merge
def merge(model, sums)->str:
    sums = model.call_model(
        prompt = merge_prompt_other,
        text = sums,
        max_token = 300
    )

    if verbose: print(sums)

    return sums


# latex
def convert_to_latex(model, summary, filename) :

    latex_code = model.call_model(latex_prompt_other, summary, 600)
    if verbose: print(latex_code)

    latex = Latex(latex_code, filename)

    compile_result = latex.compile()
    return compile_result,latex_code

# if __name__=="__main__":
#     convert_to_latex(merge(summarize([papers])))
def refine_latex(model,previous_latex_code,compile_result,filename):
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
    filename = "1"
    st.title("Latex code generator of multiple scientific texts")

    model_name = st.selectbox(
        "Model",
        ("HuggingFaceTB/SmolLM2-1.7B-Instruct", "openbmb/MiniCPM-2B-dpo-bf16", "Qwen/Qwen2.5-1.5B-Instruct")
    )
    model = Model(model_name)
    texts = get_text()

    if st.button("Generate PDFs"):
            texts = [text for text in texts if text]

            if texts: 
                sums = summarize(model, texts)
                merged_summary = merge(model, sums)
                compile_result,latex_code = convert_to_latex(model, merged_summary, filename)
                refined_result , refined_code = refine_latex(previous_latex_code=latex_code, compile_result=compile_result,filename=filename)
                if refined_result==compile_result or refined_result=="pdf is created":
                    st.success(f"PDF generated successfully!")
                    with open(f"{filename}.pdf", mode="rb") as f:
                        st.download_button(f"Download PDF", f, file_name = f"{filename}.pdf")
                else:
                    st.warning(f"Couldn't create pdf after 5 attempt...")    
            else:
                st.warning(f"No input. Skipping...")

if __name__ == "__main__":
    main()

