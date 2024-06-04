import ollama
import time
import importlib
import ProblemSetReader
import os

importlib.reload(ProblemSetReader)
problem_set_reader = ProblemSetReader.ProblemSetReader()
df = problem_set_reader.get_dataframe()
questions = list(problem_set_reader.get_dataframe()["question"])


# def create_prompt(question, example_question, example_solution):
#     str = (
#         "Please provide Python code to solve the following question with a step-by-step explanation of the thought process (Chain of Thought): "
#         + question
#         + "\n\n# Example Question:\n"
#         + example_question
#         + "\n\n# Example Solution with Chain of Thought:\n"
#         + example_solution
#         + "\n\n# Chain of Thought for the current problem:\n"
#         + "1. Understand the problem and identify the main components or requirements.\n"
#         + "2. Break down the problem into smaller, manageable steps.\n"
#         + "3. Outline the logical steps needed to solve the problem.\n"
#         + "4. Implement the solution step-by-step in Python.\n"
#         + "5. Verify the correctness of the solution.\n\n"
#         + "Please start the code with 'Code Begin' and end the code with 'Code End.'"
#     )
#     prompt = get_prompt(str)
#     return prompt


# # Example usage:
# question = "Find the sum of all the multiples of 3 or 5 below 1000."
# example_question = "If we list all the natural numbers below $10$ that are multiples of $3$ or $5$, we get $3, 5, 6$ and $9$. The sum of these multiples is $23$. Find the sum of all the multiples of $3$ or $5$ below $1000$."
# example_solution = """# Computers are fast, so we can implement this solution directly without any clever math.
# def compute():
#     ans = sum(x for x in range(1000) if (x % 3 == 0 or x % 5 == 0))
#     return str(ans)

# if __name__ == "__main__":
#     print(compute())"""


# Use following if gpu available


solution_dir = "solution"
# start_time = time.time()

for idx, row in df.iterrows():
    index = row["idx"]
    question = row["question"]

    str = (
        " You should act as a professional coder and math solver. Then Provide python code to solve the following question, the output of code should be either float or integer type: "
        + question
        + "You should start code with 'Code Begin' and end code with 'Code End."
    )
    try:
        for attempt in range(10):
            # This will run __call__()
            answer = ollama.generate(model="llama3", prompt=str)["response"]
            start_idx = answer.find("Code Begin") + len("Code Begin") + 1
            end_idx = answer.find("Code End")
            # print(answer)
            if start_idx != -1 and end_idx != -1:
                # Extract the solution code
                solution_code = answer[start_idx:end_idx].strip()

                # Generating a unique filename based on the current timestamp
                filename = f"p{idx:03d}_{attempt}.py"
                filepath = os.path.join(solution_dir, filename)

                # Write the solution code to a new file
                with open(filepath, "w") as file:
                    file.write(solution_code)
                print(f"Solution saved to {filepath}")

                # # Generating a unique filename based on the current timestamp
                # filename = f"solution_{i:03}.txt"
                # filepath = os.path.join(solution_dir, filename)

                # # Write the solution code to a new file
                # with open(filepath, "w") as file:
                #     file.write(solution_code)
                # print(f"Solution saved to {filepath}")

        else:
            print("Code tags not found in the response.")
        # time_taken = time.time() - start_time
        # print(f"Time taken: {time_taken} seconds")
    except Exception as e:
        print(f"An error occurred: {e}")
