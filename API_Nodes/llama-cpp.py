import sys
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
venv_site_packages = os.path.join(parent_dir, 'venv', 'Lib', 'site-packages')
sys.path.append(venv_site_packages)

try:
    from llama_cpp import Llama
except ImportError:
    import sys
    import os

    # Determine the correct path based on the operating system
    if os.name == 'posix':
        site_packages = os.path.join(sys.prefix, 'lib', 'python{}.{}/site-packages'.format(sys.version_info.major, sys.version_info.minor))
    else:  # For Windows
        site_packages = os.path.join(sys.prefix, 'Lib', 'site-packages')

    sys.path.append(site_packages)
    from llama_cpp import Llama

class llamacpp:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Model": ("STRING", {"default": "dolphin-2.1-mistral-7b.Q5_K_M.gguf"})
            },
            "optional": {
                "model_path": ("STRING", {"default": None}),
                "n_ctx": ("INT", {"default": 2048})
            }
        }

    RETURN_TYPES = ("LLM",)
    FUNCTION = "execute"
    CATEGORY = "AutoGen/LLM"

    def execute(self, Model, n_ctx, model_path=None):
        if model_path==None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(base_dir)
            model_path = os.path.join(parent_dir, 'models')
        model_path = os.path.join(model_path, Model)
        llm = Llama(model_path=model_path, chat_format="llama-2", n_ctx=n_ctx)


        return ({"LLM": llm, "llama-cpp": True},)

NODE_CLASS_MAPPINGS = {
    "llama-cpp": llamacpp,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "llama-cpp": "llama-cpp"
}