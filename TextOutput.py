import os


class TextOutput:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Output_Text": ("TEXT",),
                "filename_prefix": ("STRING", {"default": "AutoGen"}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save_text"
    OUTPUT_NODE = True
    CATEGORY = "AutoGen"

    def save_text(self, Output_Text, filename_prefix="ComfyUI"):
        def dict_to_string(data_dict):
            result = []
            for key, value in data_dict.items():
                if isinstance(value, dict):
                    inner_dict_str = ', '.join([f'{k}: {v}' for k, v in value.items()])
                    result.append(f'{key}: {{{inner_dict_str}}}')
                else:
                    result.append(f'{key}: {value}')
            return '{' + ', '.join(result) + '}'
        output_dir = os.path.abspath("output_folder")
        self.output_dir = output_dir
        self.type = "output"
        self.text = ""
        self.text = dict_to_string(Output_Text['TEXT'])

        full_output_folder = os.path.join(self.output_dir, "TextOutput")

        if os.path.commonpath((self.output_dir, os.path.abspath(full_output_folder))) != self.output_dir:
            print("Saving text outside the output folder is not allowed.")
            return {}

        try:
            counter = max([int(f[:-4].split('_')[-1]) for f in os.listdir(full_output_folder) if f.startswith(filename_prefix) and f.endswith('.txt')]) + 1
        except ValueError:
            counter = 1
        except FileNotFoundError:
            os.makedirs(full_output_folder, exist_ok=True)
            counter = 1

        file = f"{filename_prefix}_{counter:05}.txt"
        with open(os.path.join(full_output_folder, file), 'w', encoding='utf-8') as text_file:
            text_file.write(self.text)

        print("Text saved")

        return {}

NODE_CLASS_MAPPINGS = {
    "TextOutput": TextOutput,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "TextOutput": "LogAll"
}