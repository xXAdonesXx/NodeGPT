class Conditioning:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("TEXT",),
                "clip": ("CLIP",)
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"
    CATEGORY = "AutoGen"

    def encode(self, clip, text):
        text = text['TEXT']
        return ([[clip.encode(text), {}]], )

NODE_CLASS_MAPPINGS = {
    "Conditioning": Conditioning,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Conditioning": "Conditioning"
}