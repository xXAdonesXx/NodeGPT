import sys
sys.path.append("x:\\programme\\python\\lib\\site-packages")

import autogen  # or whatever module inside pyautogen you wish to use


class GroupChat:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "LLM": ("LLM",),
                "User": ("User",),
                "Agent": ("Agent",),
                "Agent2": ("Agent",)
            },
            "optional": {
                "Agent3": ("Agent",),
                "Agent4": ("Agent",),
                "Agent5": ("Agent",),
                "max_round": ("INT", {"default": 50}),
                "Seed": ("INT", {"default": "42"}),
                "Temp": ("INT", {"default": "0"}),
                "request_timeout": ("INT", {"default": 120})
            }
        }

    RETURN_TYPES = ("Agent",)
    FUNCTION = "execute"
    CATEGORY = "AutoGen"

    def execute(self, LLM, User,  Agent, Agent2, Seed, Temp, request_timeout, Agent3=None, Agent4=None, Agent5=None, max_round=50):
        Agents = [User['User']]

        # Function to handle agent input
        def handle_agent_input(agent_input):
            if agent_input:
                if isinstance(agent_input['Agent'], list):
                    Agents.extend(agent_input['Agent'])
                else:
                    Agents.append(agent_input['Agent'])

        # Handle each agent input
        handle_agent_input(Agent)
        handle_agent_input(Agent2)
        handle_agent_input(Agent3)
        handle_agent_input(Agent4)
        handle_agent_input(Agent5)

        groupchat = autogen.GroupChat(agents=Agents, messages=[],
                                      max_round=max_round)

        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={ #THIS has to be HERE for some reason??!!?!
                         "seed": Seed,  # seed for caching and reproducibility
                         "config_list": LLM['LLM'],  # a list of OpenAI API configurations
                         "temperature": Temp,  # temperature for sampling
                         "request_timeout": request_timeout,
                     },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
        )

        return ({"Agent": manager},)


NODE_CLASS_MAPPINGS = {
    "GroupChat": GroupChat,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "GroupChat": "GroupChat with Manager"
}