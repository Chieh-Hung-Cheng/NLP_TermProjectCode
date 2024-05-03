import os
import pickle
import pandas as pd


class ProblemSetReader:
    def __init__(self):
        """ Remeber to download the "euler_df.pkl" file and place it under "data" folder
        """
        self.base_path = os.getcwd()
        self.data_path = os.path.join(self.base_path, "data")

        self.dataframe = pd.read_pickle(os.path.join(self.data_path, "euler_df.pkl"))
        self.available_indicies_set = set(self.dataframe["idx"])
        self.available_indicies_list = sorted(list(self.available_indicies_set))

    def get_answer(self, idx):
        """Get the answer for problem {idx}

        Args:
            idx (int): the index of the problem

        Returns:
            Union(int, float, str, tuple): Return the answer. If the answer is a fraction, 
            a tuple will be returned
        """
        assert idx in self.available_indicies_set
        return self.dataframe[self.dataframe["idx"] == idx]["answer"].values[0]
    
    def get_question(self, idx):
        """Get the question for problem {idx}

        Args:
            idx (int): the index of the problem

        Returns:
            str: the question
        """
        assert idx in self.available_indicies_set
        return self.dataframe[self.dataframe["idx"] == idx]["question"].values[0]
    
    def get_python_code(self, idx):
        """Get the reference python code for problem {idx}

        Args:
            idx (int): the index of the problem

        Returns:
            str: the reference python code
        """
        assert idx in self.available_indicies_set
        return self.dataframe[self.dataframe["idx"] == idx]["python_code"].values[0]
    
    def get_problem_set(self, idx):
        """Get a tuple of (question, answer, python_code) for problem {idx}

        Args:
            idx (int): the index of the problem

        Returns:
            tuple(str, Union(int, float, str, tuple), str): a tuple of (question, answer, python_code)
        """
        answer = self.get_answer(idx)
        question = self.get_question(idx)
        python_code = self.get_python_code(idx)

        return (question, answer, python_code)
    
    def get_dataframe(self):
        """Get the original dataframe

        Returns:
            pandas.DataFrame: a dataframe containing "idx", "question", "answer", "python_code"
        """
        return self.dataframe
    
    def get_available_indicies_set(self):
        """Get the unordered set of problem indicies that has answers

        Returns:
            set: the unordered set of available indicies
        """
        return self.available_indicies_set
    
    def get_available_indicies_list(self):
        """Get the ordered list of problem indicies that has answers

        Returns:
            list: the ordered list of available indicies
        """
        return self.available_indicies_list

if __name__ == "__main__":
    problem_set_reader = ProblemSetReader()
    print(problem_set_reader.get_problem_set(1))