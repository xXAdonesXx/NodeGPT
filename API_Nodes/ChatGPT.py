class ChatGPT:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Model": ("STRING", {"default": "gpt-4"}),
                "API_Key": ("STRING", {"default": "<your OpenAI API key here>"})
            }
        }

    RETURN_TYPES = ("LLM",)
    FUNCTION = "execute"
    CATEGORY = "AutoGen/LLM"

    def execute(self, Model, API_Key):

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