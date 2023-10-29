import importlib
import os


node_list = [ #Add list of .py files containing nodes here
    "API_Nodes.ChatGPT",
    "Agents.Assistant",
    "Agents.UserProxy",
    "Chat",
    "TextOutput",
    "API_Nodes.oobaboogaOpenAI",
    "API_Nodes.Ollama",
    "DisplayText",
    "DisplayTextAsImage",
    "Agents.Engineer",
    "Groupchat",
    "Agents.AppendAgent",
    "Agents.Planner",
    "Agents.Executor",
    "Agents.Critic",
    "Agents.Scientist",
    "API_Nodes.LM_Studio",
    "TextGeneration",
    "Conditioning",
    "Output2String",
    "LoadAPIconfig"
]

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for module_name in node_list:
    imported_module = importlib.import_module(".{}".format(module_name), __name__)

    NODE_CLASS_MAPPINGS = {**NODE_CLASS_MAPPINGS, **imported_module.NODE_CLASS_MAPPINGS}
    NODE_DISPLAY_NAME_MAPPINGS = {**NODE_DISPLAY_NAME_MAPPINGS, **imported_module.NODE_DISPLAY_NAME_MAPPINGS}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
