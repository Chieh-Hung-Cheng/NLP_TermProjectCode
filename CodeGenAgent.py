from transformers import AutoTokenizer, AutoModelForCausalLM

class CodeGenAgent:
    def __init__(self, size="2B", data="mono"):
        checkpoint = f"Salesforce/codegen-{size}-{data}"
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint, padding_side="left")
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(checkpoint)

    
    def generate_batch(self, texts, max_length=256, no_repeat_input=True):
        tokenizer_out = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
        input_ids = tokenizer_out.input_ids
        attention_mask = tokenizer_out.attention_mask

        completions = self.model.generate(input_ids=input_ids,
                                         attention_mask=attention_mask,
                                         max_length=max_length)
        
        if no_repeat_input:
            completions = [completions[i][len(input_ids[i]):] for i in range(len(input_ids))]
        
        decoded_texts = self.tokenizer.batch_decode(completions, skip_special_tokens=True)

        return decoded_texts


if __name__ == "__main__":
    agent = CodeGenAgent()
    from ProblemSetReader import ProblemSetReader
    problem_set_reader = ProblemSetReader()
    sample_indicies = [3,39,40]
    problems = [problem_set_reader.get_question(idx)+'"""' for idx in sample_indicies]

    for generated_code in agent.batch_generate(problems):
        print(generated_code)







