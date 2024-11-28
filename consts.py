papers = """
Deep learning allows computational models that are composed of multiple processing layers to learn representations of data with multiple levels of abstraction. These methods have dramatically improved the state-of-the-art in speech recognition, visual object recognition, object detection and many other domains such as drug discovery and genomics. Deep learning discovers intricate structure in large data sets by using the backpropagation algorithm to indicate how a machine should change its internal parameters that are used to compute the representation in each layer from the representation in the previous layer. Deep convolutional nets have brought about breakthroughs in processing images, video, speech and audio, whereas recurrent nets have shone light on sequential data such as text and speech.
---
Broadly speaking, we can distinguish between two classes of geometric learning problems. In the first class of problems, the goal is to characterize the structure of the data. The second class of problems deals with analyzing functions defined on a given non-Euclidean domain. These two classes are related, because understanding the properties of functions defined on a domain conveys certain information about the domain, and vice versa, the structure of the domain imposes certain properties on the functions on it.
---
Dimensionality reduction involves mapping a set of high dimensional input points onto a low dimensional manifold so that “similar” points in input space are mapped to nearby points on the manifold. We present a method called Dimensionality Reduction by Learning an Invariant Mapping (DrLIM) for learning a globally coherent non-linear function that maps the data evenly to the output manifold. The learning relies solely on neighborhood relationships and does not require any distance measure in the input space. The method can learn mappings that are invariant to certain transformations of the inputs, as is demonstrated with a number of experiments. Comparisons are made to other techniques, in particular LLE.
---
In mathematics, the Pythagorean theorem or Pythagoras' theorem is a fundamental relation in Euclidean geometry between the three sides of a right triangle. It states that the area of the square whose side is the hypotenuse (the side opposite the right angle) is equal to the sum of the areas of the squares on the other two sides.
---
The theorem can be written as an equation relating the lengths of the sides a, b and the hypotenuse c, sometimes called the Pythagorean equation:[1]

    a 2 + b 2 = c 2 

The theorem is named for the Greek philosopher Pythagoras, born around 570 BC. The theorem has been proved numerous times by many different methods – possibly the most for any mathematical theorem. The proofs are diverse, including both geometric proofs and algebraic proofs, with some dating back thousands of years.

When Euclidean space is represented by a Cartesian coordinate system in analytic geometry, Euclidean distance satisfies the Pythagorean relation: the squared distance between two points equals the sum of squares of the difference in each coordinate between the points.

The theorem can be generalized in various ways: to higher-dimensional spaces, to spaces that are not Euclidean, to objects that are not right triangles, and to objects that are not triangles at all but n-dimensional solids. 
---
"""


summary_prompt = """
As an academic writer, I want you to summarize this part of my paper in one paragraph and explain terms with proper mathematics: 

"""

summary_prompt_other = """
As an academic writer, I want you to summarize the input in only one paragraph and explain terms with proper mathematics 

"""


merge_prompt_other = """
As an academic writer, I want you to write a text based on the input
"""


latex_prompt = """
As a latex expert, I want you to convert this text to proper latex code with all the formulas(ONLY ouput latex code nothing else): 


"""

latex_prompt_other = """
Generate simple LaTeX code for the input text beginning with ONLY \documentclass{article} \begin{document} and ending with ONLY \end{document}. You MUST put the LaTeX code in ONLY ```.
"""

refine_prompt = """
correct the latex code according to the error and output the refined version in plain text:
previous latex code: {0}
errors after compiling it: {1} 

"""


evaluation_prompt = """
As an latex code expert, evaluate these latex codes and their content of different generative models based on these criteria
1. relavent and logical content, 30 points
2. using mathematic formula, 10 points 
3. using correct latex code and format, 50 points
4. using academic voice, 10 points

now, you will be given latex codes and name of the models in this format and you should score them based on the criteria, only output the score of each part without any explanation: 

model_name1 : "latex_code_generated1"
model_name2 : "latex_code_generated2"
.
.

"""

API_KEY= "****"