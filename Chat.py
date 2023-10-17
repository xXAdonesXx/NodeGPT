import sys
sys.path.append("x:\\programme\\python\\lib\\site-packages")

import autogen  # or whatever module inside pyautogen you wish to use
import json


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
            user_object.initiate_chat(
                agent_object,
                message=Task,
            )

            # Check if the first key of the dictionary is a string representation of a list
            if isinstance(list(conversations.keys())[0], str):
                # Convert the string representation to an actual list
                content_list_str = list(conversations.keys())[0]
                content_list = json.loads(content_list_str)
            else:
                raise ValueError("Unexpected format of 'text'")

            # Extract the content from each dictionary in the list
            all_contents = [item['content'] for item in content_list if 'content' in item]

            # Get the last content from the list (or None if the list is empty)
            last_content = all_contents[-1] if all_contents else None

        return ({"TEXT": last_content, "LOG": conversations},)




NODE_CLASS_MAPPINGS = {
    "Chat": Chat,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Chat": "Chat"
}