import json
import os

class PromptManager:
    def __init__(self):
        self.prompts = {}
        self.load_default_prompts()
    
    def load_default_prompts(self):
        self.prompts = {
            "default_system": "You are a helpful AI assistant.",
            "summarize": "Summarize the following conversation in a concise way, highlighting the key points.",
            "extract_key_points": "Extract the most important points from this conversation."
        }
    
    def get_prompt(self, prompt_name, variables=None):
        prompt_template = self.prompts.get(prompt_name, self.prompts["default_system"])
        
        if variables:
            for key, value in variables.items():
                prompt_template = prompt_template.replace(f"{{{key}}}", str(value))
        
        return prompt_template
    
    def add_prompt(self, name, template):
        self.prompts[name] = template