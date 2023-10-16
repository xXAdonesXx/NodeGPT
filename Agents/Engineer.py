import sys
sys.path.append("x:\\programme\\python\\lib\\site-packages")

import autogen  # or whatever module inside pyautogen you wish to use

class Engineer:
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
        # create an AssistantAgent named "assistant"
        assistant = autogen.AssistantAgent(
            name="Engineer",
            system_message='''Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
            Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
            If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
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
    "Engineer": Engineer,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Engineer": "Engineer"
}


