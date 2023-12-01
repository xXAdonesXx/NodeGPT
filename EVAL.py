import sys
import os


class EVAL:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Python": ("STRING", {
                    "multiline": True,
                    "default": "#Outputs: c_bool,c_int,c_float,d_string,c_Number\nif a_int==1:\n     c_bool=True\nelse:\n    c_bool=False"}),
            },
            "optional": {
                "a_bool": ("BOOLEAN", {"default": "1"}),
                "b_bool": ("BOOLEAN", {"default": "1"}),
                "a_int": ("INT", {"default": "1"}),
                "b_int": ("INT", {"default": "1"}),
                "a_float": ("float", {"default": "1"}),
                "b_float": ("float", {"default": "1"}),
                "a_string": ("STRING", {"default": "1"}),
                "b_string": ("STRING", {"default": "1"}),
                "c_string": ("STRING", {"default": "1"})
            }
        }

    RETURN_TYPES = ("BOOLEAN","INT","Float","STRING","NUMBER",)
    FUNCTION = "EVAL"

    CATEGORY = "utils"

    def EVAL(self, Python, a_bool=None, b_bool=None, a_int=None, b_int=None, a_float=None, b_float=None, a_string=None,
             b_string=None, c_string=None):

        exec(Python)

        return (c_bool, c_int, c_float, d_string, c_Number,)

NODE_CLASS_MAPPINGS = {
    "EVAL": EVAL,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "EVAL": "EVAL"
}
