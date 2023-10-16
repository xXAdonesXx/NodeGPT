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

        # Check if the first key of the dictionary is a string representation of a list
        if isinstance(list(text.keys())[0], str):
            # Convert the string representation to an actual list
            content_list_str = list(text.keys())[0]
            content_list = json.loads(content_list_str)
        else:
            raise ValueError("Unexpected format of 'text'")

        # Extract the content from each dictionary in the list
        all_contents = [item['content'] for item in content_list if 'content' in item]

        # Get the last content from the list (or None if the list is empty)
        last_content = all_contents[-1] if all_contents else None
        print(last_content)

        return {"ui": {"text": last_content}}

NODE_CLASS_MAPPINGS = {
    "DisplayString": DisplayString,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "DisplayString": "DisplayText"
}