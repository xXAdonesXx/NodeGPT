import json
class DisplayString:
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

    RETURN_TYPES = ()
    FUNCTION = "display_text"

    OUTPUT_NODE = True

    CATEGORY = "AutoGen"

    def display_text(self, text):

        text = text['TEXT']
        print("------------------------------------------------")
        print("Last Response:")
        print("------------------------------------------------")
        print(text)

        return {"ui": {"text": text}}

NODE_CLASS_MAPPINGS = {
    "DisplayString": DisplayString,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "DisplayString": "DisplayText"
}