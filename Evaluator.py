import os
import sys

from io import StringIO
import subprocess



class Evaluator:
    def __init__(self):
        pass
    
    def compare_answer(self, truth, predicted, verbose=False)->bool:
        if (type(truth)!=type(predicted)):
            if (type(truth)==int or type(truth)==float):
                predicted = type(truth)(predicted)
            elif type(truth)==list:
                predicted = predicted.split("/")
        if verbose:
            print(f"{truth=}, {predicted=}")
        
        return truth == predicted

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
            return self.compare_answer(answer_truth, redirected_output.getvalue(), verbose)
        return False
    
    def evaluate_subprocess(self, code_path, answer_truth, verbose=False, timeout=10):
        code = open(code_path, "r").read()
        p = subprocess.Popen([sys.executable, "-c", code], 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE, 
                             text=True)
        failed = False
        try: 
            stdout, stderr = p.communicate(timeout=timeout)
            if stderr:
                if verbose: print(f"Execution Error")
                failed = True
        except subprocess.TimeoutExpired:
            if verbose: print(f"Timeout Error")
            p.kill()
            stdout, stderr = p.communicate()
            failed = True

        if not failed:
            if verbose: print("Execution Success")
            return self.compare_answer(answer_truth, stdout, verbose)
        return False
        

if __name__ == "__main__":
    from ProblemSetReader import ProblemSetReader
    problem_set_reader = ProblemSetReader()
    sample_question, sample_answer = problem_set_reader.get_problem_set(1), problem_set_reader.get_answer(1)


    evaluator = Evaluator()
    code_path = "./data/generated/p002.py"
    print(evaluator.evaluate_subprocess(code_path, sample_answer, verbose=True))

    

