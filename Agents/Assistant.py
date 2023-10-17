import sys
sys.path.append("x:\\programme\\python\\lib\\site-packages")

import autogen  # or whatever module inside pyautogen you wish to use

class Assistant:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "LLM": ("LLM",),
                "name": ("STRING", {"default": "assistant"}),
                "system_message": ("STRING", {"default": "You are a helpful assistant"})
            },
            "optional": {
                "Seed": ("INT", {"default": "42"}),
                "Temp": ("INT", {"default": "0"}),
                "request_timeout": ("INT", {"default": 120})
            }
        }

    RETURN_TYPES = ("Agent",)
    FUNCTION = "execute"
    CATEGORY = "AutoGen/Agents"

    def execute(self, LLM, name, system_message, Seed, Temp, request_timeout):
        # create an AssistantAgent named "assistant"
        assistant = autogen.AssistantAgent(
            name=name,
            system_message=system_message,
            llm_config={
                "seed": Seed,  # seed for caching and reproducibility
                "config_list": LLM['LLM'],  # a list of OpenAI API configurations
                "temperature": Temp,  # temperature for sampling
                "request_timeout": request_timeout,
            },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
        )
        return ({"Agent": assistant},)

NODE_CLASS_MAPPINGS = {
    "Assistant": Assistant,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Assistant": "Assistant"
}


