import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer


class LLamaAgent:
    def __init__(self, model_name="meta-llama/Meta-Llama-3-8B"):
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=model_name,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device="cuda",
        )

        # self.model = AutoModelForCausalLM.from_pretrained(model_name)
        # self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def generate_batch(self, texts, max_new_tokens=256):
        pass