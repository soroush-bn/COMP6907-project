# Latex code generator of multiple scientific texts 

# Overview

The Latex code generator utilizes different large language models (LLMs) to extract summaries from multiple scientific texts, generate concise summaries from the extracted outputs, and Convert the generated summaries into LaTeX format.


## models used

https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct<br>
https://huggingface.co/openbmb/MiniCPM-2B-dpo-bf16<br>
https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct<br>
https://platform.openai.com/docs/models#gpt-3-5-turbo

# Installation

```bash
## Clone the repository:
git clone https://github.com/soroush-bn/COMP6907-project.git

## Navigate to the package directory:
cd COMP6907-project

## Install required libraries:
pip install -r requirements.txt
```

# File Descriptions

## pipeline.py 
The main pipeline for generating scientific LaTeX documents from multiple input texts. It processes user inputs, generates summaries, merges them, and converts the final text into LaTeX code, which is then refined and compiled into PDF format. The script also supports evaluation and similarity analysis of LaTeX code using different models.

## models.py
Defines a "Model" class that facilitates interaction with various Large Language Models (LLMs), implements various LLMs, and supports tasks such as text embedding, token counting, similarity calculation, and model-based text generation for LaTeX and other tasks.

## consts.py
Consists of prompts for different tasks such as generating summaries, merging, refining LaTeX code, and evaluation. For the GPT model, an API key should be provided.

## latex.py
Defines a "Latex" class to convert raw LaTeX text into a .tex file, compile it into a PDF file, and extract and return relevant LaTeX error messages from the compilation logs if PDF generation fails.

## latex_codes.txt
Defined as the "file_dir" variable in pipeline.py. It stores generated and refined LaTeX codes for debugging, re-generation, and analysis tasks such as evaluation and similarity comparison.

## utils.py
Handles tasks including monitoring GPU resources, cleaning up memory, and providing detailed GPU statistics.

## requirements.txt
Lists all Python dependencies required for the package.


# Usage
```bash
# for running the code
streamlit run pipeline.py

# streamlit provide a web interface to:
#Input scientific texts, select a model for processing, generate summaries, merge them, and convert them into downloadable PDFs files.
```

# Contributing

1- Fork the repository.<br>
2- Create a new branch (git checkout -b feature/your-feature-name).<br>
3- Commit your changes (git commit -m "Add your message here").<br>
4- Push to the branch (git push origin feature/your-feature-name).<br>
5- Open a pull request.


# License

This project was created for educational purposes as part of the Data Mining Techniques/Methods course at Memorial University of Newfoundland.
