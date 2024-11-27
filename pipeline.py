from latex import Latex
from consts import *
from gpt import call_chatgpt
from models import Model
from fpdf import FPDF
import streamlit as st


verbose = True
model = Model("HuggingFaceTB/SmolLM2-1.7B-Instruct")

def get_text():
    # user input in streamlit
    text1 = st.text_area("Text 1", height=200)
    text2 = st.text_area("Text 2", height=200)
    text3 = st.text_area("Text 3", height=200)

    return [text1, text2, text3]

#2 summarize
def summarize(texts):
    summary =  ""
    for text in texts:
        summary += model.call_model(
            prompt = summary_prompt,
            text = text,
            max_token = 300
        )
        # summary+=(call_chatgpt(summary_prompt+text,300,API_KEY))
    if verbose: print(summary)
    return summary


#3 merge
def merge(sums)->str:
    sums = model.call_model(
        prompt = merge_prompt_other,
        text = sums,
        max_token = 300
    )

    if verbose: print(sums)

    return sums


# latex
def convert_to_latex(summary, filename) :

    latex_code = model.call_model(latex_prompt_other, summary, 600)
    if verbose: print(latex_code)

    latex = Latex(latex_code, filename)

    print(latex.compile())

# if __name__=="__main__":
#     convert_to_latex(merge(summarize([papers])))



def main():
    filename = "1"
    st.title("Latex code generator of multiple scientific texts")

    # Get text from user input (via Streamlit)
    texts = get_text()

    # Button to trigger the background process
    if st.button("Generate PDF"):
        # Ensure all text areas have been filled
        if all(texts):
            # Step 1: Summarize the texts
            summary = summarize(texts)

            # Step 2: Merge summaries into one paragraph
            merged_summary = merge(summary)

            # Step 3: Convert merged summary to LaTeX and generate PDF
            convert_to_latex(merged_summary, filename)

            # Provide the user with a download button for the generated PDF
            st.success("PDF generated successfully!")
            with open(f"{filename}.pdf", mode = "rb") as f:
                st.download_button("Download PDF", f, file_name = "summary_output.pdf")
        else:
            st.error("Please fill in all the text areas.")

if __name__ == "__main__":
    main()
























