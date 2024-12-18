import os  

class Latex():
    def __init__(self,text, name) -> None:
        self.raw_text =text
        self.name = name

    def __to_tex(self):
        with open(f"./outputs/{self.name}.tex", "w") as file:
            file.write(self.raw_text)

    def compile(self):
        self.__to_tex()
        os.system(f"pdflatex -halt-on-error -output-directory=outputs ./outputs/{self.name}.tex")
        if not self.__check_pdf_exists():
            return self.__get_logs()
        else:
            return "pdf is created"

    
    def __check_pdf_exists(self):

        if os.path.isfile(f"./outputs/{self.name}" +".pdf"):
            return True
        else:
            return False

    def __get_logs(self):
        try:
            with open(f"./outputs/{self.name}.log", "r") as file:
                log_content = file.read()
            idx1= log_content.find("LaTeX Error")
            idx2= log_content.find("See the LaTeX")

            return log_content[idx1:idx2]
        except FileNotFoundError:
            return f"Error: The file ./outputs/{self.name}.log does not exist."
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
