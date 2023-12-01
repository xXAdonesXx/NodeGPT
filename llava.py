import sys
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
venv_site_packages = os.path.join(base_dir, 'venv', 'Lib', 'site-packages')
sys.path.append(venv_site_packages)

try:
    from llama_cpp import Llama
    from llama_cpp.llama_chat_format import Llava15ChatHandler
    import numpy as np
    from PIL import Image
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
    from llama_cpp.llama_chat_format import Llava15ChatHandler
    import numpy as np
    from PIL import Image

class llava:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "Model": ("STRING", {"default": "ggml-model-q4_k.gguf"}),
                "Clip_Model": ("STRING", {"default": "mmproj-model-f16.gguf"}),
                "system_message": ("STRING", {"default": "You are an assistant who perfectly describes images."}),
                "Prompt": ("STRING", {
                    "multiline": True,
                    "default": "Describe this image in detail please."
                }),
            },
            "optional": {
                "models_path": ("STRING", {"default": None}),
                "n_ctx": ("INT", {"default": 2048}),
                "n_gpu_layers": ("INT", {"default": 0}),
                "temp": ("FLOAT", {"default": 0.1})

            }
        }

    RETURN_TYPES = ("TEXT",)
    FUNCTION = "execute"
    CATEGORY = "AutoGen"

    def execute(self, image, Model, Clip_Model, n_ctx, system_message, Prompt, temp, n_gpu_layers, models_path=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if models_path==None:
            models_path = os.path.join(base_dir, 'models')
        model_path = os.path.join(models_path, Model)
        clip_model_path = os.path.join(models_path, Clip_Model)

        first_image = image[0]  # Access the first image
        img = 255.0 * first_image.cpu().numpy()  # Adjust if your tensor doesn't require .cpu()
        img = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))

        # Save the first image
        temp_dir = os.path.join(base_dir, 'temp')
        first_frame_file = os.path.join(temp_dir, 'temp_img.png')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        img.save(first_frame_file)

        chat_handler = Llava15ChatHandler(clip_model_path=clip_model_path)
        llm = Llama(
            model_path=model_path,
            chat_format="llava-1-5",
            chat_handler=chat_handler,
            n_ctx=n_ctx,  # n_ctx should be increased to accomodate the image embedding
            logits_all=True,
            verbose=True
        )
        file_url = f"file:///{first_frame_file}"
        response =llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system_message},
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": file_url}},
                        {"type": "text", "text": Prompt}
                    ]
                }
            ]
        , temperature=temp)

        response = response['choices'][0]['message']['content']
        print(response)
        return ({"TEXT": response},)

NODE_CLASS_MAPPINGS = {
    "llava": llava,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "llava": "llava"
}