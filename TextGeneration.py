import sys
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
venv_site_packages = os.path.join(base_dir, 'venv', 'Lib', 'site-packages')
sys.path.append(venv_site_packages)
from autogen import oai

class TextGeneration:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "LLM": ("LLM",),
                "use_cache": ("STRING", {"default": "False"}),
                "timeout": ("INT", {"default": 120}),
                "system_message": ("STRING", {"default": "You are a helpful AI assistant"}),
                "Prompt": ("STRING", {
                    "multiline": True,
                    "default": "Your Prompt"
                }),
            }
        }

    RETURN_TYPES = ("TEXT",)
    FUNCTION = "execute"
    CATEGORY = "AutoGen"

    def execute(self, LLM, Prompt, system_message, use_cache, timeout):
        if use_cache == "True":
            use_cache=True
        else:
            use_cache=False
        if LLM['llama-cpp']==True:
            llm=LLM['LLM']
            response=llm.create_chat_completion(
                  messages = [
                      {"role": "system", "content": system_message},
                      {
                          "role": "user",
                          "content": Prompt
                      }
                  ]
                )
        else:
            response = oai.ChatCompletion.create(
                config_list = LLM['LLM'],
                messages=[
                    {"role": "system",
                     "content": system_message},
                    {"role": "user", "content": Prompt}],
                use_cache=use_cache,
                timeout=timeout,
                )
        response = response['choices'][0]['message']['content']
        return ({"TEXT": response},)

NODE_CLASS_MAPPINGS = {
    "TextGeneration": TextGeneration,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "TextGeneration": "TextGeneration"
}


