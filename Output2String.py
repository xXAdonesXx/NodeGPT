import json
class Output2String:
    def __init__(self):
        self.type = "output"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("TEXT",),
            },
            "hidden": {},
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"
    CATEGORY = "AutoGen"

    def execute(self, text):

        text = text['TEXT']
        print("------------------------------------------------")
        print("Last Response:")
        print("------------------------------------------------")
        print(text)

        return(text,);

NODE_CLASS_MAPPINGS = {
    "Output2String": Output2String,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Output2String": "Output2String"
}
