
import sys
import autogen

class Scientist:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "LLM": ("LLM",)
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

    def execute(self, LLM, Seed, Temp, request_timeout):
        # create an AssistantAgent named "scientist"
        scientist = autogen.AssistantAgent(
            name="Scientist",
            system_message='''Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed. You don't write code.''',
            llm_config={
                "seed": Seed,
                "config_list": LLM['LLM'],
                "temperature": Temp,
                "request_timeout": request_timeout,
            },
        )
        return ({"Agent": scientist},)

NODE_CLASS_MAPPINGS = {
    "Scientist": Scientist,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Scientist": "Scientist"
}
