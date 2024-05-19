import os
import pandas as pd

import pickle
import urllib.request
from tqdm import tqdm

class DataProcessor: 
    def __init__(self) -> None:
        self.base_path = os.getcwd()
        self.data_path = os.path.join(self.base_path, "data")
        self.python_path = os.path.join(self.data_path, "python")

        self.answers = None
        self.process_answers()

        if not os.path.isdir(os.path.join(self.data_path, "questions")):
            os.mkdir(os.path.join(self.data_path, "questions"))
        self.question_path = os.path.join(self.data_path, "questions")

    def get_python_code(self, idx):
        with open (os.path.join(self.python_path, f"p{idx:03d}.py")) as f:
            ret_str = ""
            for line in f:
                if line.startswith("#"):
                    continue
                else:
                    ret_str += line
            return ret_str 
    
    def process_answers(self):
        self.answers = {}
        with open(os.path.join(self.data_path, "Answers.txt")) as f:
            for line in f:
                if not line.startswith("Problem"): 
                    continue
                
                problem_index = int(line[8:11])
                answer_str = line[13:-1]
                
                if '/' in answer_str:
                    continue
                if not answer_str.isnumeric():
                    continue
                
                answer_float = float(answer_str)
                self.answers[problem_index] = answer_float
    
    def get_answer(self, idx):
        assert idx in self.answers
        return self.answers[idx]
                    
    def get_question(self, idx):
        if not os.path.isfile(os.path.join(self.question_path, f"p{idx:03d}.txt")):
            self.download_question(idx)
        
        with open(os.path.join(self.question_path, f"p{idx:03d}.txt"), "r", encoding="utf-8") as f:
            return f.read()
    
    def get_available_indicies(self):
        answer_idxes = list(self.answers.keys())

        available_idxes = [idx for idx in answer_idxes \
                           if os.path.isfile(os.path.join(self.python_path, f"p{idx:03d}.py")) ]
        return available_idxes
    
    def download_question(self, idx):
        fp = urllib.request.urlopen(f"https://projecteuler.net/minimal={idx}")
        str = fp.read().decode("utf-8")
        # remove html tags
        import re
        str = re.sub("<.*?>", "", str)
        with open(os.path.join(self.question_path, f"p{idx:03d}.txt"), "w", encoding="utf-8") as f:
            f.write(str)

    def get_euler_dataframe(self):
        availalbe_idx = self.get_available_indicies()
        answers = [ self.get_answer(idx) for idx in availalbe_idx ]
        questions = [ self.get_question(idx) for idx in availalbe_idx ]
        python_codes = [ self.get_python_code(idx) for idx in availalbe_idx ]

        df = pd.DataFrame({
            "idx": availalbe_idx,
            "question": questions,
            "answer": answers,
            "python_code": python_codes
        }).sort_values(by="idx")
        return df

    

if __name__ == "__main__":
    data_processor = DataProcessor()
    df = data_processor.get_euler_dataframe()
    # save df
    df.to_pickle("./data/euler_df.pkl")
