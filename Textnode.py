import os
import requests

output_dir = os.path.abspath("output_folder")
server = "127.0.0.1"  # define the server address here

PARAMS = {
    'max_new_tokens': 200,
    'temperature': 0.5,
    'top_p': 0.9,
    'typical_p': 1,
    'n': 1,
    'stop': None,
    'do_sample': True,
    'return_prompt': False,
    'return_metadata': False,
    'typical_p': 0.95,
    'repetition_penalty': 1.05,
    'encoder_repetition_penalty': 1.0,
    'top_k': 0,
    'min_length': 0,
    'no_repeat_ngram_size': 2,
    'num_beams': 1,
    'penalty_alpha': 0,
    'length_penalty': 1.0,
    'pad_token_id': None,
    'eos_token_id': None,
    'use_cache': True,
    'num_return_sequences': 1,
    'bad_words_ids': None,
    'seed': -1,
}

class TextInput:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {
                    "multiline": True,
                    "default": "Enter text here"
                })
            }
        }
        
    RETURN_TYPES = ("CUSTOM",)
    FUNCTION = "execute"
    CATEGORY = "Text"
    
    def execute(self, input_text):
        return ({"text": input_text},)


class TextOutput:
    def __init__(self):
        self.output_dir = output_dir
        self.type = "output"
        self.text = ""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_data": ("CUSTOM", {"input_format": {"text": "STRING"}}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save_text"
    OUTPUT_NODE = True
    CATEGORY = "Text"

    def save_text(self, input_data, filename_prefix="ComfyUI"):
        input_text = input_data.get("text")
        self.text = input_text

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
            text_file.write(input_text)

        return {"text": input_text}

    def ui(self):
        return {"ui": [
            {
                "type": "textarea",
                "label": "Output text",
                "id": "output_text",
                "value": self.text
            }
        ]}


class TextGenerator:

    do_sample = True
    early_stopping = False
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_name": ("STRING", {"default": "gpt2"}),
                "prompt_text": ("CUSTOM", {"input_format": {"text": "STRING"}}),
            },
            "optional": {
                "max_new_tokens": ("INT", {"default": PARAMS['max_new_tokens']}),
                "temperature": ("FLOAT", {"default": PARAMS['temperature']}),
                "top_p": ("FLOAT", {"default": PARAMS['top_p']}),
                "typical_p": ("FLOAT", {"default": PARAMS['typical_p']}),
                "repetition_penalty": ("FLOAT", {"default": PARAMS['repetition_penalty']}),
                "encoder_repetition_penalty": ("FLOAT", {"default": PARAMS['encoder_repetition_penalty']}),
                "top_k": ("INT", {"default": PARAMS['top_k']}),
                "min_length": ("INT", {"default": PARAMS['min_length']}),
                "no_repeat_ngram_size": ("INT", {"default": PARAMS['no_repeat_ngram_size']}),
                "num_beams": ("INT", {"default": PARAMS['num_beams']}),
                "penalty_alpha": ("FLOAT", {"default": PARAMS['penalty_alpha']}),
                "length_penalty": ("FLOAT", {"default": PARAMS['length_penalty']}),
                "seed": ("INT", {"default": PARAMS['seed']})
            }
        }
        
    RETURN_TYPES = ("CUSTOM",)
    FUNCTION = "generate_text"
    CATEGORY = "Text"
    
    def generate_text(self, model_name, prompt_text, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed):
        self.model_name = model_name
        self.prompt_text = prompt_text.get("text", "")
        self.max_new_tokens = max_new_tokens
        self.do_sample = TextGenerator.do_sample
        self.temperature = temperature
        self.top_p = top_p
        self.typical_p = typical_p
        self.repetition_penalty = repetition_penalty
        self.encoder_repetition_penalty = encoder_repetition_penalty
        self.top_k = top_k
        self.min_length = min_length
        self.no_repeat_ngram_size = no_repeat_ngram_size
        self.num_beams = num_beams
        self.penalty_alpha = penalty_alpha
        self.length_penalty = length_penalty
        self.early_stopping = TextGenerator.early_stopping
        self.seed = seed
        
        # Make request to API to generate text
        url = f"http://{server}:7860/run/textgen"
        headers = {"Content-Type": "application/json"}
        data = {
            "data": [
                self.prompt_text,
                self.max_new_tokens,
                self.do_sample,
                self.temperature,
                self.top_p,
                self.typical_p,
                self.repetition_penalty,
                self.encoder_repetition_penalty,
                self.top_k,
                self.min_length,
                self.no_repeat_ngram_size,
                self.num_beams,
                self.penalty_alpha,
                self.length_penalty,
                self.early_stopping,
                self.seed
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        
        # Check for errors in API response
        if response.status_code != 200:
            self.generated_text = None
            print(f"Error generating text: {response.text}")
            return {}
        
        # Parse generated text from API response
        response_data = response.json()["data"]
        if len(response_data) < 1:
            self.generated_text = None
            print("Error generating text: Empty response from API")
            return {}
        generated_text = response_data[0]
        
        # Save generated text and return it
        self.generated_text = generated_text
        return ({"text": generated_text},)

class TextCombine:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_data_1": ("CUSTOM", {"input_format": {"text": "STRING"}}),
                "input_data_2": ("CUSTOM", {"input_format": {"text": "STRING"}})
            }
        }
        
    RETURN_TYPES = ("CUSTOM",)
    FUNCTION = "execute"
    CATEGORY = "Text"
    
    def execute(self, input_data_1, input_data_2):
        input_text_1 = input_data_1.get("text")
        input_text_2 = input_data_2.get("text")
        combined_text = input_text_1 + input_text_2
        
        return ({"text": combined_text},)

class StableDiffusion:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("CUSTOM", {"input_format": {"text": "STRING"}}),
                "clip": ("CLIP", )
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"
    CATEGORY = "Text"

    def encode(self, clip, text):
        input_text = text.get("text")
        return ([[clip.encode(input_text), {}]], )

# A dictionary that contains all nodes you want to export with their names
NODE_CLASS_MAPPINGS = {
    "TextInput": TextInput,
    "TextOutput": TextOutput,
    "TextGenerator": TextGenerator,
    "TextCombine": TextCombine,
    "StableDiffusion": StableDiffusion
    
}

