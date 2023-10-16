
import sys
sys.path.append("x:\\programme\\python\\lib\\site-packages")

import autogen

class Critic:
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
    CATEGORY = "AutoGen"

    def execute(self, LLM, Seed, Temp, request_timeout):
        # create an AssistantAgent named "critic"
        critic = autogen.AssistantAgent(
            name="Critic",
            system_message='''Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.''',
            llm_config={
                "seed": Seed,
                "config_list": LLM['LLM'],
                "temperature": Temp,
                "request_timeout": request_timeout,
            },
        )
        return ({"Agent": critic},)

NODE_CLASS_MAPPINGS = {
    "Critic": Critic,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Critic": "Critic"
}
