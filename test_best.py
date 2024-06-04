import importlib
import ProblemSetReader
import pandas as pd
import os

importlib.reload(ProblemSetReader)
problem_set_reader = ProblemSetReader.ProblemSetReader()
df = problem_set_reader.get_dataframe()

from Evaluator import Evaluator

evaluator = Evaluator()
answer_paths = {
    "llama3": "./best_solution",
    "gpt4": "./best_solution_gpt",
    "code_gen": "./best_solution_gen",
}

results_df = pd.DataFrame(
    columns=[
        "idx",
        "llama3",
        "gpt4",
        "code_gen",
        "result_llama3",
        "result_gpt4",
        "result_code_gen",
    ]
)

for idx in df["idx"].values:
    row = {
        "idx": idx,
        "llama3": 0,
        "gpt4": 0,
        "code_gen": 0,
        "result_llama3": "",
        "result_gpt4": "",
        "result_code_gen": "",
    }
    for key, answer_path in answer_paths.items():
        file_name = f"p{idx:03d}.py"
        code_path = os.path.join(answer_path, file_name)

        if not os.path.exists(code_path):
            continue

        answer_truth = problem_set_reader.get_answer(idx)
        result = evaluator.evaluate_subprocess(code_path, answer_truth, verbose=False)

        if result == "correct answer":
            row[key] = 1
            row[f"result_{key}"] = result
        else:
            row[f"result_{key}"] = result

    results_df = pd.concat([results_df, pd.DataFrame([row])], ignore_index=True)

results_df.to_csv("evaluation_results.csv", index=False)
