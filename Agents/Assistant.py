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


