from g4f.client import Client


class GPTAgent:

    def __init__(self):
        self.client = Client()

    def generate_chain_of_thoughts(self, question, prefix=None, suffix=None):

        prefix = "List the procedure for writing code to solve the problem. \
                Return the procedures in list and without explaining. \
                Each line should be the number of bullet, plus the procedure. (e.g. 2. {procedure})\
                If a certain step is within a loop, specify them.\
                The last step should be printing the answer. \
                Do not return any code, only the procedure." if prefix is None else prefix
        suffix = "" if suffix is None else suffix

        content = prefix + question + suffix

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": content}]
        )

        ret_string = response.choices[0].message.content
        return ret_string
    
    def generate_code(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        ret_string = response.choices[0].message.content
        return ret_string
    



if __name__ == "__main__":
    agent = GPTAgent()
    from ProblemSetReader import ProblemSetReader
    problem_set_reader = ProblemSetReader()
    
    print(agent.generate_chain_of_thoughts(question=problem_set_reader.get_question(1)))
