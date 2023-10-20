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
