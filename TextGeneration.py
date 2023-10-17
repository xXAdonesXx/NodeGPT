import sys
from autogen import oai

class TextGeneration:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "LLM": ("LLM",),
                "use_cache": ("STRING", {"default": "False"}),
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

    def execute(self, LLM, Prompt, system_message, use_cache):
        if use_cache == "True":
            use_cache=True
        else:
            use_cache=False
        response = oai.ChatCompletion.create(
            config_list = LLM['LLM'],
            messages=[
                {"role": "system",
                 "content": system_message},
                {"role": "user", "content": Prompt}],
            use_cache=use_cache,
            )
        response = response['choices'][0]['message']['content']

        return ({"TEXT": response},)

NODE_CLASS_MAPPINGS = {
    "TextGeneration": TextGeneration,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "TextGeneration": "TextGeneration"
}


