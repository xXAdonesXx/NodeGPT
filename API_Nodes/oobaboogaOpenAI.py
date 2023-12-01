class oobaboogaOpenAI:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("STRING", {"default": "gpt-3.5-turbo"}),
                "api_key": ("STRING", {"default": "any string here is fine"}),
                "api_type": ("STRING", {"default": "openai"}),
                "api_base": ("STRING", {"default": "http://127.0.0.1:5001/v1"}),
                "api_version": ("STRING", {"default": "2023-05-15"})
            }
        }

    RETURN_TYPES = ("LLM",)
    FUNCTION = "execute"
    CATEGORY = "AutoGen/LLM"

    def execute(self, model, api_key, api_type, api_base, api_version):
        config_list = [
            {
                'model': model,
                'api_key': api_key,
                'api_type': api_type,
                'api_base': api_base,
                'api_version': api_version,

            }
        ]
        return ({"LLM": config_list, "llama-cpp": False},)

NODE_CLASS_MAPPINGS = {
    "oobaboogaOpenAI": oobaboogaOpenAI,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "oobaboogaOpenAI": "oobaboogaOpenAI"
}