class LM_Studio:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_base": ("STRING", {"default": "http://localhost:1234/v1"}),
                "api_key": ("STRING", {"default": "NULL"})
            }
        }

    RETURN_TYPES = ("LLM",)
    FUNCTION = "execute"
    CATEGORY = "AutoGen/LLM"

    def execute(self, api_base, api_key):
        config_list = [
            {
                'api_key': api_key,
                'base_url': api_base,
            }
        ]
        return ({"LLM": config_list, "llama-cpp": False},)

NODE_CLASS_MAPPINGS = {
    "LM_Studio": LM_Studio,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LM_Studio": "LM Studio"
}