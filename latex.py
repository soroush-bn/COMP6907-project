import os  
import re

class Latex():
    def __init__(self,text, name) -> None:
        self.raw_text =text
        self.name = name

    def __to_tex(self):
        with open(f"{self.name}.tex", "w") as file:
            file.write(self.raw_text)
    def __pre_process(self):
        pass
    def compile(self):
        self.__to_tex()
        os.system(f"pdflatex -halt-on-error {self.name}.tex")
        if not self.__check_pdf_exists():
            return self.__get_logs()
        else:
            return "pdf is created"

    
    def __check_pdf_exists(self):

        if os.path.isfile(self.name +".pdf"):
            return True
        else:
            return False

    def __get_logs(self):
        try:
            # Open the .log file in read mode
            with open(f"{self.name}.log", "r") as file:
                # Read the file's contents into a string
                log_content = file.read()
                pattern = r"^! LaTeX error.*?\.$"
    
            matches = re.findall(pattern, log_content, re.MULTILINE)

            for e in matches:
                log_content+=e 
            return log_content
        except FileNotFoundError:
            return f"Error: The file {self.name}.log does not exist."
        except Exception as e:
            return f"An error occurred: {e}"


if __name__=="__main__":
    t =r"""\sdf
\documentclass{article}
\begin{document}
  Hello World!
\end{document}
"""
    latex = Latex(t)
    latex.to_tex()
    latex.compile()
