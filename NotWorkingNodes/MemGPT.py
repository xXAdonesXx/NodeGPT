import sys
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
venv_site_packages = os.path.join(parent_dir, 'venv', 'Lib', 'site-packages')
sys.path.append(venv_site_packages)

try:
    import autogen
    import memgpt.autogen.memgpt_agent as memgpt_autogen
    import memgpt.autogen.interface as autogen_interface
    import memgpt.agent as agent
    import memgpt.system as system
    import memgpt.utils as utils
    import memgpt.presets as presets
    import memgpt.constants as constants
    import memgpt.personas.personas as personas
    import memgpt.humans.humans as humans
    from memgpt.persistence_manager import InMemoryStateManager, InMemoryStateManagerWithPreloadedArchivalMemory, InMemoryStateManagerWithFaiss

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
    import memgpt.autogen.memgpt_agent as memgpt_autogen
    import memgpt.autogen.interface as autogen_interface
    import memgpt.agent as agent
    import memgpt.system as system
    import memgpt.utils as utils
    import memgpt.presets as presets
    import memgpt.constants as constants
    import memgpt.personas.personas as personas
    import memgpt.humans.humans as humans
    from memgpt.persistence_manager import InMemoryStateManager, InMemoryStateManagerWithPreloadedArchivalMemory, InMemoryStateManagerWithFaiss


class MemGPT:
    @classmethod
    def INPUT_TYPES(cls):
        return {

        }

    RETURN_TYPES = ("Agent",)
    FUNCTION = "execute"
    CATEGORY = "AutoGen/Agents"

    def execute(self):
        interface = autogen_interface.AutoGenInterface()  # how MemGPT talks to AutoGen
        persistence_manager = InMemoryStateManager()
        persona = "I\'m a 10x engineer at a FAANG tech company."
        human = "I\'m a team manager at a FAANG tech company."
        memgpt_agent = presets.use_preset(presets.DEFAULT, 'gpt-4', persona, human, interface, persistence_manager)

        # MemGPT coder
        coder = memgpt_autogen.MemGPTAgent(
            name="MemGPT_coder",
            agent=memgpt_agent,
        )
        return ({"Agent": coder},)

NODE_CLASS_MAPPINGS = {
    "MemGPT": MemGPT,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "MemGPT": "MemGPT"
}


