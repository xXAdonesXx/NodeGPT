import sys
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
venv_site_packages = os.path.join(parent_dir, 'venv', 'Lib', 'site-packages')
sys.path.append(venv_site_packages)
import autogen


class UserProxy:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "name": ("STRING", {"default": "User"}),
                "human_input_mode": ("STRING", {"default": "TERMINATE"}),
                "system_message": ("STRING", {"default": "Reply TERMINATE if the task has been solved at full satisfaction. Otherwise, reply CONTINUE, or the reason why the task is not solved yet."}),
                "default_auto_reply": ("STRING", {"default": "Reply TERMINATE if you are done"}),
                "code_execution": ("STRING", {"default": "True"}),
                "code_execution_dir": ("STRING", {"default": "coding"}),
                "MaxConsecutiveAutoReply": ("INT", {"default": "10"}),
                "Terminate_Token": ("STRING", {"default": "TERMINATE"})
            },
            "optional": {
                "LLM": ("LLM",),

            }
        }

    RETURN_TYPES = ("User",)
    FUNCTION = "execute"
    CATEGORY = "AutoGen"

    def execute(self, name, human_input_mode, system_message, code_execution, code_execution_dir, MaxConsecutiveAutoReply, Terminate_Token, default_auto_reply, LLM=None):
        # create an AssistantAgent named "assistant"
        if code_execution=="True":
            code_execution_config = {
                "work_dir": code_execution_dir,
                "use_docker": False  # set to True or image name like "python:3" to use docker
            }
        else:
            code_execution_config = False
        if LLM==None:
            user_proxy = autogen.UserProxyAgent(
                name=name,
                human_input_mode=human_input_mode,
                system_message=system_message,
                max_consecutive_auto_reply=MaxConsecutiveAutoReply,
                is_termination_msg=lambda x: x.get("content", "").rstrip().endswith(Terminate_Token),
                code_execution_config=code_execution_config,
                default_auto_reply=default_auto_reply,
            )
        else:
            user_proxy = autogen.UserProxyAgent(
                name=name,
                human_input_mode=human_input_mode,
                system_message=system_message,
                max_consecutive_auto_reply=MaxConsecutiveAutoReply,
                is_termination_msg=lambda x: x.get("content", "").rstrip().endswith(Terminate_Token),
                code_execution_config=code_execution_config,
                default_auto_reply=default_auto_reply,
                llm_config={
                "seed": 42,  # seed for caching and reproducibility
                "config_list": LLM['LLM'],  # a list of OpenAI API configurations
                "temperature": 0,  # temperature for sampling
                "request_timeout": 120,
                },
            )


        return ({"User": user_proxy},)

NODE_CLASS_MAPPINGS = {
    "UserProxy": UserProxy,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "UserProxy": "UserProxy"
}
