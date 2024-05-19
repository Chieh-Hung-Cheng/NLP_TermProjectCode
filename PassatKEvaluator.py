import os
import subprocess
import re
import pandas as pd
from Evaluator import Evaluator
import ProblemSetReader

class PassAtKEvaluator(Evaluator):
    def __init__(self):
        super().__init__()

    def evaluate_pass_at_k(self, folder_path, problem_set_df, k=1, verbose=False):
        ret_dict = {
            "pass_at_k_count": 0,
            "total_count": 0
        }

        for idx in problem_set_df["idx"].values:
            correct_found = False

            for attempt in range(k):
                file_name = f"p{idx:03d}_{attempt}.py"
                code_path = os.path.join(folder_path, file_name)

                if not os.path.exists(code_path):
                    continue

                answer_truth = ProblemSetReader().get_answer(idx)
                result = self.evaluate_subprocess(code_path, answer_truth, verbose)

                if result == "correct answer":
                    correct_found = True
                    break

            ret_dict["total_count"] += 1
            if correct_found:
                ret_dict["pass_at_k_count"] += 1

        ret_dict["pass_at_k_ratio"] = ret_dict["pass_at_k_count"] / ret_dict["total_count"]
        return ret_dict