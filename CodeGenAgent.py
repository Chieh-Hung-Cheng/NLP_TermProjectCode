import os
import torch

from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM

class CodeGenAgent:
    def __init__(self, size="2B", data="mono"):
        self.base_path = os.getcwd()
        self.data_path = os.path.join(self.base_path, "data")
        self.generated_path = os.path.join(self.data_path, "generated")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        checkpoint = f"Salesforce/codegen-{size}-{data}"
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint, padding_side="left")
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(checkpoint).to(self.device)


    def _get_larger_power_of_2(self, num):
        return 2 ** num.bit_length()

    def generate_batch(self, 
                       texts,
                       max_new_tokens=256, 
                       no_repeat_input=True):
        tokenizer_out = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True).to(self.device)

        input_ids = tokenizer_out.input_ids
        attention_mask = tokenizer_out.attention_mask
        
        completions = self.model.generate(input_ids=input_ids,
                                        attention_mask=attention_mask,
                                        max_new_tokens=max_new_tokens)
        
        if no_repeat_input:
            completions = [completions[i][len(input_ids[i]):] for i in range(len(input_ids))]
        
        decoded_texts = self.tokenizer.batch_decode(completions, skip_special_tokens=True)

        return decoded_texts

    def generate_code_for_indicies(self, 
                                   problem_indicies, 
                                   batch_size=8, 
                                   no_repeat_input=True):
        from ProblemSetReader import ProblemSetReader
        problem_set_reader = ProblemSetReader()


        num_batches = len(problem_indicies) // batch_size if len(problem_indicies) % batch_size == 0 \
            else len(problem_indicies) // batch_size + 1
        
        for i in tqdm(range(num_batches)):
            indicies_batch = problem_indicies[i*batch_size:(i+1)*batch_size]
            problems = [problem_set_reader.get_question(idx)+'"""' for idx in indicies_batch]

            problems = [x for x in problems if len(x)<2048/4]
            if (len(problems)==0): continue

            generated_codes = self.generate_batch(problems,
                                                  no_repeat_input=no_repeat_input)
            for idx, generated_code in zip(indicies_batch, generated_codes):
                with open(os.path.join(self.generated_path, f"p{idx:03d}.py"), "w", encoding="utf-8") as f:
                    f.write(generated_code)
            
        

if __name__ == "__main__":
    agent = CodeGenAgent()
    from ProblemSetReader import ProblemSetReader
    problem_set_reader = ProblemSetReader()
    
    agent.generate_code_for_indicies(list(range(17, 25)))







