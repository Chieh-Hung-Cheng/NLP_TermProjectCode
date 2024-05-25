import os
import pandas as pd
from Evaluator import Evaluator


class HumanEvalHelper:
    def __init__(self):
        self.base_path = os.getcwd()
        self.data_path = os.path.join(self.base_path, "data")

        self.prompt_eval_df = pd.read_csv(os.path.join(self.data_path, "prompt_eval.csv"))
        self.evaluator = Evaluator()

    def show_questions_sequentailly(self, start=0):
        for idx, row in self.prompt_eval_df.iterrows():
            if (row["idx"]<start): continue
            print(f"Problem {row['idx']}:\n {row['question']}\n\n{row['best_GPT4code']}")
            # wait until user input

            print(self.evaluator.evaluate_subprocess(os.path.join(self.data_path, "best_gpt4_codes", f"p{idx:03d}.py"), row['answer'], verbose=True))
            

            input()
            # clear console
            os.system('cls||clear')

if __name__ == "__main__":
    helper = HumanEvalHelper()
    helper.show_questions_sequentailly(start=118)
        