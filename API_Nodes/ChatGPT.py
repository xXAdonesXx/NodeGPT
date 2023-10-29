import sys
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(base_dir, 'API_Configs')


class ChatGPT:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Model": ("STRING", {"default": "gpt-4"})
            },
            "optional": {
                "API_Key": ("STRING", {"default": None})
            }
        }

    RETURN_TYPES = ("LLM",)
    FUNCTION = "execute"
    CATEGORY = "AutoGen/LLM"

    def execute(self, Model, API_Key):
        if API_Key is None:
            with open(os.path.join(folder_path, "OpenAI.txt"), 'r') as file:
                API = file.read().strip()
            config_list = [
                {
                    'model': Model,
                    'api_key': API,
                }
            ]
        else:
            config_list = [
                {
                    'model': Model,
                    'api_key': API_Key,
                }
            ]

        return ({"LLM": config_list},)

NODE_CLASS_MAPPINGS = {
    "ChatGPT": ChatGPT,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ChatGPT": "ChatGPT"
}