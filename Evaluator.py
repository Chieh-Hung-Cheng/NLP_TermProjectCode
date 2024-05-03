import os
import sys

from io import StringIO
import subprocess
import re
import time


class Evaluator:
    def __init__(self):
        pass
    
    def compare_answer(self, truth, predicted, verbose=False)->bool:
        

        if verbose:
            print(f"{truth=}, {predicted=}")

        if (len(predicted)==0 ): return False

        predicted = predicted.strip()

        if '/' in predicted:
            try:
                predicted = predicted.split("/")
            except:
                return False
        elif '.' in predicted:
            try:
                predicted = float(predicted)
            except:
                return False

        if (type(truth)!=type(predicted)):
            if (type(truth)==int or type(truth)==float):
                try: 
                    predicted = type(truth)(predicted)
                except:
                    return False
            elif type(truth)==list:
                try:
                    predicted = predicted.split("/")
                except:
                    return False
                if len(predicted) != len(truth):
                    return False
        if verbose:
            print(f"{truth=}, {predicted=}")
        
        return truth == predicted
    
    
    def evaluate_subprocess(self, code_path, answer_truth, verbose=False, timeout=30):
        """Use a subprocess with time limit to evaluate the correctness of the (generated) code

        Args:
            code_path (os.path): the file path of the (generated) code
            answer_truth (Union(int, float, str, list)): the ground truth of the answer
            verbose (bool, optional): whether to print out the result of the code. Defaults to False.
            timeout (int, optional): when to kill the process if it takes too long. Defaults to 10.

        Returns:
           str: "runtime error", "timeout error", "correct answer", "wrong answer"
        """
        # code = open(code_path, "r").read()
        p = subprocess.Popen(["python", code_path], 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE, 
                             text=True)

        failed = False
        try: 
            stdout, stderr = p.communicate(timeout=timeout)
            if stderr:
                if verbose: print(f"Execution Error")
                return "runtime error"
        except subprocess.TimeoutExpired:
            if verbose: print(f"Timeout Error")
            p.kill()
            stdout, stderr = p.communicate()
            return "timeout error"

        if self.compare_answer(answer_truth, stdout, verbose):
            if verbose: print(f"Correct Answer")
            return "correct answer"
        else:
            if verbose: print(f"Wrong Answer")
            return "wrong answer"
        
    
    def evaluate_folder(self, folder_path, problem_set_df, timeout=20):
        dirs = os.listdir(folder_path)

        ret_dict = {}
        ret_dict["correct_count"] = 0
        ret_dict["wrong_count"] = 0
        ret_dict["timeout_count"] = 0
        ret_dict["runtimeerr_count"] = 0
        ret_dict["missing_count"] = 0

        for dir in dirs:
            print(dir)
            # get only files with format p{idx:03d}.py
            code_path = os.path.join(folder_path, dir)
            if os.path.isdir(code_path): continue
            if not re.match("p[0-9][0-9][0-9].py", dir): continue
            idx = int(dir[1:4])
            answer_truth = problem_set_df[problem_set_df["idx"] == idx]["answer"].values[0]

            result = self.evaluate_subprocess(code_path, answer_truth, verbose=True, timeout=timeout)
            if (result == "correct answer"):
                ret_dict["correct_count"] += 1
            elif (result == "wrong answer"):
                ret_dict["wrong_count"] += 1
            elif (result == "timeout error"):
                ret_dict["timeout_count"] += 1
            elif (result == "runtime error"):
                ret_dict["runtimeerr_count"] += 1
        
        ret_dict["missing_count"] = problem_set_df["idx"].count() - (ret_dict["correct_count"] + ret_dict["wrong_count"] + ret_dict["timeout_count"] + ret_dict["runtimeerr_count"])

        ret_dict["correct_ratio"] = ret_dict["correct_count"] / problem_set_df["idx"].count()
        ret_dict["wrong_ratio"] = ret_dict["wrong_count"] / problem_set_df["idx"].count()
        ret_dict["timeout_ratio"] = ret_dict["timeout_count"] / problem_set_df["idx"].count()
        ret_dict["runtimeerr_ratio"] = ret_dict["runtimeerr_count"] / problem_set_df["idx"].count()
        ret_dict["missing_ratio"] = ret_dict["missing_count"] / problem_set_df["idx"].count()

        return ret_dict 
            

if __name__ == "__main__":
    from ProblemSetReader import ProblemSetReader
    problem_set_reader = ProblemSetReader()

    evaluator = Evaluator()
    # code_path = "./data/generated/p001.py"
    # print(evaluator.evaluate_subprocess(code_path, problem_set_reader.get_answer(1), verbose=True))
    code_folder_path = "./data/generated"
    print(evaluator.evaluate_folder(code_folder_path, 
                                    problem_set_reader.get_dataframe()))

    

