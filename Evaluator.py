import os
import sys

from io import StringIO




class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, code_path, answer_truth):
        code = open(code_path, "r").read()

        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        try: 
            exec(code)
        except:
            raise Exception("Error in code")
        finally: 
            sys.stdout = old_stdout
        
        answer_calculated = redirected_output.getvalue()
        
        if answer_calculated != str(answer_truth):
            return True
        else:
            return False

        

if __name__ == "__main__":
    evaluator = Evaluator()
    code_path = "./data/python/p001.py"
    print(evaluator.evaluate(code_path))
    

