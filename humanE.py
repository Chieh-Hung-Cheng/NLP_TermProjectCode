import pandas as pd
import importlib
import ProblemSetReader

importlib.reload(ProblemSetReader)
problem_set_reader = ProblemSetReader.ProblemSetReader()
df_solution = problem_set_reader.get_dataframe()

df = pd.read_csv("prompt_eval.csv")

scores = []

for index, row in df.iterrows():
    matching_row = df_solution[df_solution["idx"] == row["idx"]]

    if not matching_row.empty:
        solution = matching_row.iloc[0]["python_code"]
        print(f"Solution code:\n{solution}\n")

    print(f"Python Code:\n{row['best_GPT4code']}\n")

    correctness = int(input("Enter correctness score (1-5): "))
    efficiency = int(input("Enter efficiency score (1-5): "))
    readability = int(input("Enter readability score (1-5): "))

    scores.append([row["idx"], correctness, efficiency, readability])

# Create a new dataframe with the scores
scores_df = pd.DataFrame(
    scores, columns=["idx", "correctness", "efficiency", "readability"]
)

# Save the scores dataframe to a CSV file
scores_df.to_csv("humanAnnotate.csv", index=False)

print("Scores saved to scores.csv")
