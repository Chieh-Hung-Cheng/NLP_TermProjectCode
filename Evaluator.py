import os
import sys

from io import StringIO
import subprocess



class Evaluator:
    def __init__(self):
        pass
    
    
    def evaluate(self, code_path, answer_truth, verbose=False):
        code = open(code_path, "r").read()

        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        
        failed = False
        try: 
            exec(code)
        except:
            failed = True
        finally: 
            sys.stdout = old_stdout
        
        if not failed:
            answer_calculated = redirected_output.getvalue()
            if (type(answer_truth)==int or type(answer_truth)==float):
                answer_calculated = type(answer_truth)(answer_calculated)
            elif type(answer_truth)==list:
                answer_calculated = answer_calculated.split("/")

            if verbose:
                print(f"{answer_calculated=}, {answer_truth=}")

            return answer_calculated == answer_truth

        if verbose:
            print("execution failed")
        return False

        

if __name__ == "__main__":
    from ProblemSetReader import ProblemSetReader
    problem_set_reader = ProblemSetReader()
    sample_question, sample_answer = problem_set_reader.get_problem_set(1), problem_set_reader.get_answer(1)


    evaluator = Evaluator()
    code_path = "./data/python/p001.py"
    print(evaluator.evaluate(code_path, sample_answer, verbose=True))

    

