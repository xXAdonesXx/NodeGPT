import sys
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

class Planner:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "LLM": ("LLM",)
            },
            "optional": {
                "cache_seed": ("INT", {"default": "42"}),
                "Temp": ("INT", {"default": "0"}),
                "timeout": ("INT", {"default": 120})
            }
        }

    RETURN_TYPES = ("Agent",)
    FUNCTION = "execute"
    CATEGORY = "AutoGen/Agents"

    def execute(self, LLM, cache_seed, Temp, timeout):
        # create an AssistantAgent named "assistant"
        assistant = autogen.AssistantAgent(
            name="Planner",
            system_message='''Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
            The plan may involve an engineer who can write code and a scientist who doesn't write code.
            Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
            ''',
            llm_config={
                "cache_seed": cache_seed,  # cache_seed for caching and reproducibility
                "config_list": LLM['LLM'],  # a list of OpenAI API configurations
                "temperature": Temp,  # temperature for sampling
                "timeout": timeout,
            },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
        )
        return ({"Agent": assistant},)

NODE_CLASS_MAPPINGS = {
    "Planner": Planner,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Planner": "Planner"
}


