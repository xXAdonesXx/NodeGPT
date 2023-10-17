import sys
sys.path.append("x:\\programme\\python\\lib\\site-packages")

import autogen  # or whatever module inside pyautogen you wish to use

class Planner:
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
        # create an AssistantAgent named "assistant"
        assistant = autogen.AssistantAgent(
            name="Planner",
            system_message='''Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
            The plan may involve an engineer who can write code and a scientist who doesn't write code.
            Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
            ''',
            llm_config={
                "seed": Seed,  # seed for caching and reproducibility
                "config_list": LLM['LLM'],  # a list of OpenAI API configurations
                "temperature": Temp,  # temperature for sampling
                "request_timeout": request_timeout,
            },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
        )
        return ({"Agent": assistant},)

NODE_CLASS_MAPPINGS = {
    "Planner": Planner,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Planner": "Planner"
}


