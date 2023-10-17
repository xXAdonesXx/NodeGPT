class AppendAgent:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Agent1": ("Agent",),
                "Agent2": ("Agent",)
            }
        }

    RETURN_TYPES = ("Agent",)
    FUNCTION = "execute"
    CATEGORY = "AutoGen/Agents"

    def execute(self,  Agent1, Agent2):
        Agents = []

        # Function to handle agent input
        def handle_agent_input(agent_input):
            if agent_input:
                if isinstance(agent_input['Agent'], list):
                    Agents.extend(agent_input['Agent'])
                else:
                    Agents.append(agent_input['Agent'])

        # Handle each agent input
        handle_agent_input(Agent1)
        handle_agent_input(Agent2)

        return ({"Agent": Agents},)


NODE_CLASS_MAPPINGS = {
    "AppendAgent": AppendAgent,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "AppendAgent": "AppendAgent"
}