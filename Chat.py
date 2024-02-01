import sys
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
venv_site_packages = os.path.join(base_dir, 'venv', 'Lib', 'site-packages')
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
    
    def execute(self, Task, User, Agent, Input,Instructions=None):
        # Validate Instructions
        if Instructions is not None and not isinstance(Instructions, str):
            raise ValueError("Instructions must be a string")
        user_object = User['User']  # Extract the actual user object from the dictionary
        agent_object = Agent['Agent']
        print(agent_object)
        for key, value in vars(agent_object).items():
            print(f"{key}: {value}")
        conversations = {}
        # autogen.ChatCompletion.start_logging(conversations)
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
            # Check if the conversations dictionary is empty
            if not conversations:
                print("Conversations is empty")
                return ({"TEXT": None, "LOG": conversations},)

            # Check if the first key of the dictionary is a string representation of a list
            if isinstance(list(conversations.keys())[0], str):
                # Convert the string representation to an actual list
                first_key = list(conversations.keys())[0]
                content_list_str = list(conversations.keys())[0]
                content_list = json.loads(content_list_str)
            else:
                raise ValueError("Unexpected format of 'text'")

            # Extract the content from each dictionary in the list
            last_content = "booo"
            all_contents = [item['content'] for item in content_list if 'content' in item]

            # Get the last content from the list (or None if the list is empty)
            last_content = all_contents[-1] if all_contents else None
            print(last_content)
            return ({"TEXT": last_content, "LOG": conversations},) if last_content is not None else ({"TEXT": "No content", "LOG": conversations},)
        # return ({"TEXT":"fooo", "LOG": conversations},)



NODE_CLASS_MAPPINGS = {
    "Chat": Chat,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Chat": "Chat"
}
