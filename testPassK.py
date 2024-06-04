import PassatKEvaluator
import importlib

importlib.reload(PassatKEvaluator)

import ProblemSetReader

importlib.reload(ProblemSetReader)
problem_set_reader = ProblemSetReader.ProblemSetReader()
df = problem_set_reader.get_dataframe()
evaluator = PassatKEvaluator.PassAtKEvaluator()
answer_path = "./solution"

result, file_names = evaluator.evaluate_pass_at_k(answer_path, df, k=10)
print(result)

import re
import shutil
import os

# Define the source and destination directories
source_dir = "./solution"
destination_dir = "./best_solution"
pattern = re.compile(r"_(\d+)\.py$")

if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

for file_name in file_names:
    source_file = os.path.join(source_dir, file_name)
    new_file_name = re.sub(pattern, ".py", file_name)
    destination_file = os.path.join(destination_dir, new_file_name)

    shutil.copy(source_file, destination_file)

print("Files copied successfully.")
