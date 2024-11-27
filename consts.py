papers = """
Abstract:
Objective: Several forward dynamics estimation approaches have been proposed to estimate individual muscle force. However, characterization of the estimation error that arises when measurements are available only from a subset of the muscles involved in the movement under analysis, as is the case of the forearm muscles, has been limited. Our objectives were: first, to quantify the accuracy of forward-dynamics muscle force estimators for forearm muscles; and second, to develop a muscle force estimator that is accurate even when measurements are available only from a subset of muscles acting on a given joint or segment. Methods: We developed a neuromusculoskeletal (NMSK) estimator that integrates forward dynamics estimation with a neural model of muscle cocontraction to estimate individual muscle force during isometric contractions, suitable to operate when measurements are not available for all muscles. We developed a computational framework to assess the effect of physiological variability in muscle cocontraction, cross-talk, and measurement error on the estimator accuracy using a sensitivity analysis. We thus compared the performance of our estimator with that of a standard estimator that neglects the contribution of unmeasured muscles. Results: The NMSK estimator reduces the estimation error by 25% in average noise conditions. Moreover, the NMSK estimator is robust against physiological variability in muscle cocontraction and outperforms the standard estimator even when the validity of the neural model is compromised. Conclusion and Significance: In isometric tasks, the NMSK estimator reduces muscle force estimation error compared to a standard estimator, and may enable future applications involving estimation of forearm muscle force during coordinated movements.
"""


summary_prompt = """
As an academic writer, I want you to summarize this part of my paper in one paragraph and explain terms with proper mathematics: 

"""

summary_prompt_other = """
As an academic writer, I want you to summarize the input in only one paragraph and explain terms with proper mathematics 

"""


latex_prompt = """
As a latex expert, I want you to convert this text to proper latex code with all the formulas(ONLY ouput latex code nothing else): 


"""

refine_prompt = """
correct the latex code according to the error and output the refined version:
latex code: {0}
error: {1} 

"""

API_KEY= "****"