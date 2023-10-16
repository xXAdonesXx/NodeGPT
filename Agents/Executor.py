
import sys
sys.path.append("x:\\programme\\python\\lib\\site-packages")

import autogen

class Executor:
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
        # create an AssistantAgent named "executor"
        executor = autogen.AssistantAgent(
            name="Executor",
            system_message='''Executor. Execute the code written by the engineer and report the result.''',
            human_input_mode="NEVER",
            code_execution_config={"last_n_messages": 3, "work_dir": "coding"},
            llm_config={
                "seed": Seed,
                "config_list": LLM['LLM'],
                "temperature": Temp,
                "request_timeout": request_timeout,
            },
        )
        return ({"Agent": executor},)

NODE_CLASS_MAPPINGS = {
    "Executor": Executor,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Executor": "Executor"
}
