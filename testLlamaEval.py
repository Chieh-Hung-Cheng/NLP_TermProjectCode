import HolisticEvaluator
import importlib
import pandas as pd

importlib.reload(HolisticEvaluator)

import ProblemSetReader

importlib.reload(ProblemSetReader)

problem_set_reader = ProblemSetReader.ProblemSetReader()
df = problem_set_reader.get_dataframe()
evaluator = HolisticEvaluator.HolisticEvaluator()
template_path = "Geval_prompt_CCH.txt"
answers_folder = "./best_solution"

prompts_df = evaluator.create_prompts_better(template_path, answers_folder, df)
final_df = evaluator.Geval(prompts_df, 5)
final_df.to_csv("prompt_df.csv", index=False)
