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

class Critic:
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
        # create an AssistantAgent named "critic"
        critic = autogen.AssistantAgent(
            name="Critic",
            system_message='''Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.''',
            llm_config={
                "cache_seed": cache_seed,
                "config_list": LLM['LLM'],
                "temperature": Temp,
                "timeout": timeout,
            },
        )
        return ({"Agent": critic},)

NODE_CLASS_MAPPINGS = {
    "Critic": Critic,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Critic": "Critic"
}
