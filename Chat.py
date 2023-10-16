import sys
sys.path.append("x:\\programme\\python\\lib\\site-packages")

import autogen  # or whatever module inside pyautogen you wish to use


class Chat:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Task": ("STRING", {
                    "multiline": True,
                    "default": "Task here"
                }),
                "User": ("User",),
                "Agent": ("Agent",),
                "Instructions": ("STRING", {
                    "multiline": True,
                    "default": "Instructions:\nDo not write anything here!\nType below in the Input \nNEW for a new chat \nSEND to send a message if asked \nAsk if you have a follow up question"
                }),
                "Input": ("STRING", {"default": "NEW"})
            }
        }

    RETURN_TYPES = ("TEXT",)
    FUNCTION = "execute"
    CATEGORY = "AutoGen"

    def execute(self, Task, User, Agent, Input, Instructions=None):
        user_object = User['User']  # Extract the actual user object from the dictionary
        agent_object = Agent['Agent']
        print(agent_object)
        conversations = {}
        autogen.ChatCompletion.start_logging(conversations)
        if Input=="SEND":
            user_object.send(
                recipient=agent_object,
                message=Task,
            )
        else:
            print(agent_object)
            user_object.initiate_chat(
                agent_object,
                message=Task,
            )

        return ({"TEXT": conversations},)




NODE_CLASS_MAPPINGS = {
    "Chat": Chat,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Chat": "Chat"
}