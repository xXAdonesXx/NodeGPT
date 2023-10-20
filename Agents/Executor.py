import sys
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
venv_site_packages = os.path.join(parent_dir, 'venv', 'Lib', 'site-packages')
sys.path.append(venv_site_packages)

try:
    import autogen
except ImportError:
    import sys
    import os

    # Determine the correct path based on the operating system
    if os.name == 'posix':
        site_packages = os.path.join(sys.prefix, 'lib', 'python{}.{}/site-packages'.format(sys.version_info.major, sys.version_info.minor))
    else:  # For Windows
        site_packages = os.path.join(sys.prefix, 'Lib', 'site-packages')

    sys.path.append(site_packages)
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
    CATEGORY = "AutoGen/Agents"

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
