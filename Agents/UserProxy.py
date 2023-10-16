import sys
sys.path.append("x:\\programme\\python\\lib\\site-packages")

import autogen  # or whatever module inside pyautogen you wish to use


class UserProxy:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "name": ("STRING", {"default": "User"}),
                "human_input_mode": ("STRING", {"default": ""}),
                "system_message": ("STRING", {"default": "ALWAYS"}),
                "code_execution": ("STRING", {"default": "True"}),
                "code_execution_dir": ("STRING", {"default": "coding"}),
                "MaxConsecutiveAutoReply": ("INT", {"default": "10"}),
                "Terminate_Token": ("STRING", {"default": "TERMINATE"})
            }
        }

    RETURN_TYPES = ("User",)
    FUNCTION = "execute"
    CATEGORY = "AutoGen"

    def execute(self, name, human_input_mode, system_message, code_execution, code_execution_dir, MaxConsecutiveAutoReply, Terminate_Token):
        # create an AssistantAgent named "assistant"
        if code_execution=="True":
            code_execution_config = {
                "work_dir": code_execution_dir,
                "use_docker": False  # set to True or image name like "python:3" to use docker
            }
        else:
            code_execution_config = False

        user_proxy = autogen.UserProxyAgent(
            name=name,
            human_input_mode=human_input_mode,
            system_message=system_message,
            max_consecutive_auto_reply=MaxConsecutiveAutoReply,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith(Terminate_Token),
            code_execution_config=code_execution_config
        )

        return ({"User": user_proxy},)

NODE_CLASS_MAPPINGS = {
    "UserProxy": UserProxy,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "UserProxy": "UserProxy"
}