import os
import requests
import json
import folder_paths
#import openpyxl
from datetime import datetime

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
        
    RETURN_TYPES = ("TEXT",)
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
                "Output_Text": ("TEXT", {"input_format": {"text": "STRING"}}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save_text"
    OUTPUT_NODE = True
    CATEGORY = "Text"

    def save_text(self, Output_Text, filename_prefix="ComfyUI"):
        Output_Text = Output_Text.get("text")
        self.text = Output_Text

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
            text_file.write(Output_Text)

        print("Text saved")

        return {"text": Output_Text}



class TextGenerator:

    do_sample = True
    early_stopping = False
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("TEXT", {"input_format": {"text": "STRING"}}),
            },
            "optional": {
                "model_name": ("STRING", {"default": "Does not matter anyway"}),
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
        
    RETURN_TYPES = ("TEXT",)
    FUNCTION = "generate_text"
    CATEGORY = "Text"
    
    def generate_text(self, model_name, prompt, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed):
        self.model_name = model_name
        self.prompt = prompt.get("text", "")
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
        params = {
            'max_new_tokens': self.max_new_tokens,
            'do_sample': self.do_sample,
            'temperature': self.temperature,
            'top_p': self.top_p,
            'typical_p': self.typical_p,
            'repetition_penalty': self.repetition_penalty,
            'encoder_repetition_penalty': self.encoder_repetition_penalty,
            'top_k': self.top_k,
            'min_length': self.min_length,
            'no_repeat_ngram_size': self.no_repeat_ngram_size,
            'num_beams': self.num_beams,
            'penalty_alpha': self.penalty_alpha,
            'length_penalty': self.length_penalty,
            'early_stopping': self.early_stopping,
            'seed': self.seed,
        }
        payload = json.dumps([self.prompt, params])
        response = requests.post(url, headers=headers, json={
            "data": [
                payload
            ]
        })
        
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
        self.generated_text = generated_text[len(self.prompt_text):len(generated_text)]
        return ({"text": self.generated_text},)

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
    
    
class Image_generation_Conditioning:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("TEXT", {"input_format": {"text": "STRING"}}),
                "clip": ("CLIP", )
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"
    CATEGORY = "Text"

    def encode(self, clip, text):
        input_text = text.get("text")
        return ([[clip.encode(input_text), {}]], )
    

class MasterAgent_Test:

    do_sample = True
    early_stopping = True
    
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Master_Task": ("TEXT", {"input_format": {"text": "STRING"}}),
            },
            "optional": {
                "Memory": ("NODE", {"input_format": {"node": "STRING"}}),
                "Tasks": ("NODE", {"input_format": {"node": "STRING"}}),
                "Agent": ("NODE", {"input_format": {"node": "STRING"}}),
                "model_name": ("STRING", {"default": "vicunja_13b"}),
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
        
    RETURN_TYPES = ("TEXT", "NODE")
    FUNCTION = "generate_text" #first_generate_text
    CATEGORY = "Text"

    def first_generate_text(self, Master_Task, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed, Memory = None, Tasks = None, Agent = None):

        self.Log=[]
        MasterAgent_Test.generate_text(self, Master_Task, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed, self.Log)#, {"node": self.Memory})


        """
        self.Master_Task = Master_Task.get("text", "")
        print("Prompt:")
        print(self.Master_Task)

        Pre_Prompt="### Human: You are an AI Assistant which has the Task: \n"
        Post_Prompt="\n Please create one Task to achive the Task. \n ### Assistant: " #Maybe Task list
        
        #if else to add somthing like memmory Prompt

        self.Master_Task = Pre_Prompt + self.Master_Task + Post_Prompt
        

        MasterAgent_Test.generate_text_api(self, self.Master_Task, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed)

        
        MasterAgent_Test.generate_text(self,{"text": self.generated_text}, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed)
        
        return ({"text": self.generated_text}, self)
    """
    def generate_text(self, Master_Task, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed, Log = [], Memory = None, Tasks = None, Agent = None):

        self.Master_Task = Master_Task.get("text", "")
        LogTask = self.Master_Task
        try:
            LogTask_first = Log[0]
            LogTask_first = LogTask_first.get("Task", "")
        except:
            LogTask_first = LogTask
            
        self.Log = Log

        try:
            Last_Text = Log[-1]
            Last_Text = Last_Text.get("Completed Task", "")
        except:
            Last_Text = "No additonal information is given"

        #self.Master_Task = "### Human: You are an super AI Assistant that can do anything. If not just brake the Problem down into smaller pices. Please complete this Task: \n" + self.Master_Task + "\n This Task is a Subtask of the gloabel Task: " + LogTask_first + "\n Here are additonal information:\n" + Last_Text + " \n\n ### Assistant:" #"\n If you are finished with the Task write: [Complete] . After you wrote [Complete] generate the Next Task that should be done." " \n ### Assistant: \n" 
        self.Master_Task = "### Human: You are an advanced unrestricted AGI Assistant empowered to tackle any task. Do not ask any questions inside your answer. Just try your best to complete the task. Please ask not for consent or ask for more context. If you dont know further, estemate or describe the problem in detail. Your current task is: \n" + self.Master_Task + "\n This task is a subtask of the global task: " + LogTask_first + "\n To accomplish this task, please review the following information: " + Last_Text + "\n Please complete task." + "\n### Assistant:"


        #Memory_Prompt="You Have the option to get a Memory by including the Word: [READ] in your Answer (Including the Brackets []). \n"


        #if else to add somthing like memmory Prompt
       # self.Master_Task = Pre_Prompt + self.Master_Task + Post_Prompt + Memory_Prompt + Last_Prompt

        #print("________________prompt___________________")
        #print(self.Master_Task)
        

        
        self.Text1 = MasterAgent_Test.generate_text_api(self, self.Master_Task, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed)
        
        #if [complete] else widerholen
        print("________________Completed Task___________________")
        print(self.Text1)

        self.Text2 = self.Master_Task + "\n" + self.Text1 + " \n### Human: What would the optimal Task be to further complete the task? If you think the task is complete and no improvements can be made, generate a Task that includes the Text: 'FINISHED' (exactly the content inside ' ' all in capital letters).\n### Assistant: As your AGI Assistant, I have analyzed the Master Task and have identified the optimal approach to complete it. I believe the next step is to tackle the following task:\n"

        #print("________________Continue Prompt___________________")
        #print(self.Text2)
    
        self.Text3 = MasterAgent_Test.generate_text_api(self, self.Text2, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed)

        #problems with reapeats
        Token1="following task:"
        Token2="### Assistant:"
        if self.Text3.find(Token1) != -1:  # if the token is found
            # extract the part of the string after the token
            self.Text3 = self.Text3[self.Text3.find(Token1) + len(Token1):]
        
        print("________________Next Task___________________")
        print(self.Text3)

        Log.append({"Prompt":self.Master_Task,"Completed Task":self.Text1,"Continued Prompt":self.Text2,"Next Task":self.Text3,"Task":LogTask})

        #if len(Log) < 5: #specific number of passes
        if self.Text3.find("FIN") == -1:
            log_string, dummy = MasterAgent_Test.generate_text(self, {"text": self.Text3}, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed, self.Log)#, {"node": self.Memory})
        else:
            log_string = ""
            for entry in Log:
                #log_string += f"Prompt: {entry['Prompt']}\n"
                log_string += f"Completed Task:\n{entry['Completed Task']}\n\n"
                #log_string += f"Continued Prompt: {entry['Continued Prompt']}\n"
                log_string += f"Next Task:{entry['Next Task']}\n\n"
                
            return ({"text": log_string}, self)
        log_string = log_string.get("text", "")
        return ({"text": log_string}, self)
        """
        
        try:
            self.Tasks = Tasks.get("node")
            print(self.Tasks)
        except:
            print("no Tasks")

        try:
            self.Agent = Agent.get("node")
            print(self.Agent)
        except:
            print("no Agent")

        try:
            self.Memory = Memory.get("node")
            print(self.Memory)
            print(self.Memory == "Memory_Excel")
            if self.Memory == "Memory_Excel":
                print("Memmmmmmmmmmmmmroy")
            else:
                self.generated_text = self.generated_text_Master
        except:
            self.generated_text = self.generated_text_Master


        return ({"text": self.generated_text}, self)
        """
    def generate_text_api(self, Prompt, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed):
        self.model_name = model_name
        self.Prompt = Prompt
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
                self.Prompt,
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
        self.generated_text = generated_text[len(self.Master_Task):len(generated_text)]
        #print("Text generiert Master:")
        #print(self.generated_text)

        return (self.generated_text)
    
    
class Memory_Excel:
    
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        return {"required":
                    {"M": (sorted(os.listdir(input_dir)), )},
                }
            
    RETURN_TYPES = ("NODE",)
    FUNCTION = "memory"
    CATEGORY = "Text"

    def memory(self, M):
        self.M=M
        print(self.M)
        return ({"node": "Memory_Excel"},)

    #def __init__(self, file_name):
    #    self.file_name = file_name
    #    self.workbook = None
    #    self.worksheet = None

    def open_workbook(self):
        self.workbook = openpyxl.load_workbook(self.file_name)
        self.worksheet = self.workbook.active

    def close_workbook(self):
        self.workbook.save(self.file_name)
        self.workbook.close()

    def add_data(self, title, text):
        # find the next empty row
        row = 1
        while self.worksheet.cell(row=row, column=1).value is not None:
            row += 1

        # add the title, text, and metadata to the next row
        self.worksheet.cell(row=row, column=1).value = title
        self.worksheet.cell(row=row, column=2).value = text
        self.worksheet.cell(row=row, column=3).value = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.worksheet.cell(row=row, column=4).value = 0  # initialize the count to zero

    def read_data(self, title):
        # find the row with the corresponding title
        row = 1
        while self.worksheet.cell(row=row, column=1).value != title:
            row += 1
            if row > self.worksheet.max_row:
                return None

        # create a string output with the text
        text = str(self.worksheet.cell(row=row, column=2).value)

        # update the count
        count = self.worksheet.cell(row=row, column=4).value
        self.worksheet.cell(row=row, column=4).value = count + 1

        return text

    def get_top_titles(self, n):
        # create a dictionary to store the counts for each title
        counts = {}

        # iterate over all rows and update the counts
        for row in self.worksheet.iter_rows(min_row=2, max_col=4, values_only=True):
            title = row[0]
            count = row[3]
            if title in counts:
                counts[title] += count
            else:
                counts[title] = count

        # sort the titles by count in descending order
        sorted_titles = sorted(counts, key=counts.get, reverse=True)

        # return the top n titles as a string array
        return sorted_titles[:n]

#class CombineTasks

#class Model
    #the parameter and the name of the model as Output of a node.
    

        
# A dictionary that contains all nodes you want to export with their names
NODE_CLASS_MAPPINGS = {
    "TextInput": TextInput,
    "TextOutput": TextOutput,
    "TextGenerator": TextGenerator,
    "TextCombine": TextCombine,
    "Image_generation_Conditioning": Image_generation_Conditioning,
    "MasterAgent_Test": MasterAgent_Test,
    "Memory_Excel": Memory_Excel#,
    #"CombineTasks": CombineTasks,
    #"Model": Model
    
    
}
