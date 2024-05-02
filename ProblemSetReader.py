import os
import pickle
import pandas as pd


class ProblemSetReader:
    def __init__(self):
        self.base_path = os.getcwd()
        self.data_path = os.path.join(self.base_path, "data")

        self.dataframe = pd.read_pickle(os.path.join(self.data_path, "euler_df.pkl"))
        self.available_indicies_set = set(self.dataframe["idx"])
        self.available_indicies_list = sorted(list(self.available_indicies_set))

    def get_answer(self, idx):
        assert idx in self.available_indicies_set
        return self.dataframe[self.dataframe["idx"] == idx]["answer"].values[0]
    
    def get_question(self, idx):
        assert idx in self.available_indicies_set
        return self.dataframe[self.dataframe["idx"] == idx]["question"].values[0]
    
    def get_python_code(self, idx):
        assert idx in self.available_indicies_set
        return self.dataframe[self.dataframe["idx"] == idx]["python_code"].values[0]
    
    def get_problem_set(self, idx):
        answer = self.get_answer(idx)
        question = self.get_question(idx)
        python_code = self.get_python_code(idx)

        return (question, answer, python_code)
    
    def get_dataframe(self):
        return self.dataframe
    
    def get_available_indicies_set(self):
        return self.available_indicies_set
    
    def get_available_indicies_list(self):
        return self.available_indicies_list

if __name__ == "__main__":
    problem_set_reader = ProblemSetReader()
    print(problem_set_reader.get_problem_set(1))