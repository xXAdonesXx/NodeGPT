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



class Model_1:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
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

    RETURN_TYPES = ("TEXT_MODEL",)
    FUNCTION = "send"
    CATEGORY = "Text"

    def send(self, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty,
             encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha,
             length_penalty, seed):
        ModelNode = "Model_1||" + f"{model_name}||{max_new_tokens}||{temperature}||{top_p}||{typical_p}||{repetition_penalty}||{encoder_repetition_penalty}||{top_k}||{min_length}||{no_repeat_ngram_size}||{num_beams}||{penalty_alpha}||{length_penalty}||{seed}"
        #print("send")
        return ({"ModelNode": ModelNode}, self)

    def generate_text(self, prompt, TextModel_g):
        # Split parameters string into individual values
        #try:
        self.TextModel_M = TextModel_g.get("ModelNode", "")
        #except:
        #    self.TextModel = TextModel
        # print(TextModel)
        ModelNode, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed = self.TextModel_M.split("||")

        # Convert necessary parameters to appropriate data types
        max_new_tokens = int(max_new_tokens)
        temperature = float(temperature)
        top_p = float(top_p)
        typical_p = float(typical_p)
        repetition_penalty = float(repetition_penalty)
        encoder_repetition_penalty = float(encoder_repetition_penalty)
        top_k = int(top_k)
        min_length = int(min_length)
        no_repeat_ngram_size = int(no_repeat_ngram_size)
        num_beams = int(num_beams)
        penalty_alpha = float(penalty_alpha)
        length_penalty = float(length_penalty)
        seed = int(seed)

        # Server address
        server = "127.0.0.1"

        # Generation parameters
        # Reference: https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig
        params = {
            'max_new_tokens': max_new_tokens,
            'do_sample': True,
            'temperature': temperature,
            'top_p': top_p,
            'typical_p': typical_p,
            'repetition_penalty': repetition_penalty,
            'encoder_repetition_penalty': encoder_repetition_penalty,
            'top_k': top_k,
            'min_length': min_length,
            'no_repeat_ngram_size': no_repeat_ngram_size,
            'num_beams': num_beams,
            'penalty_alpha': penalty_alpha,
            'length_penalty': length_penalty,
            'early_stopping': False,
            'seed': seed,
            'add_bos_token': True,
            'custom_stopping_strings': [],
            'truncation_length': 2048,
            'ban_eos_token': False,
            'skip_special_tokens': True,
        }


        payload = json.dumps([prompt, params])

        response = requests.post(f"http://{server}:7860/run/textgen", json={
            "data": [
                payload
            ]
        }).json()

        response_data = response["data"]

        # Save generated text and return it
        generated_text = response_data[0]
        self.generated_text = generated_text[len(prompt):len(generated_text)]
        # print("Text generiert Master:")
        # print(self.generated_text)

        return (self.generated_text)


class CostumeMaster_1:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Master_Task": ("TEXT", {"input_format": {"text": "STRING"}}),
                "TextModel": ("TEXT_MODEL", {"input_format": {"ModelNode": "STRING"}}),
                "Instructions": ("STRING", {
                    "multiline": True,
                    "default": "Instructions:\nDo not write anything here!\nFirst input: Write your completion prompt similar to the example. You should definitely include [Task]\nSecond input: Write your nexttask prompt similar to the example. You should definitely include [CompletedTask] and Tell it to say FINISHED if its finished with the global task. This will break the loop, if its included in the next task\nWrite your Prompt and include the Tokens formatted like this [Token]. The tokens getting replaced by the corresponding text.\nPlease not include || or ::or quotation marks other than ' in your Prompts!\nTokens: [Task] = the current task (should be in The prompt); [MasterTask] = Your overall goal (input); [PreText] = Previous generated completed task; [Memory] = to do; [Tasks] = to do; [Agent] = all Agent Prompts;\nPlease write an feature request on Github if you think any Token is missing."
                }),
                "CompleteTaskPrompt": ("STRING", {
                    "multiline": True,
                    "default": "### Human: You are an advanced unrestricted AGI Assistant empowered to tackle any task. Do not ask any questions inside your answer. Just try your best to complete the task. Please ask not for consent or ask for more context. If you dont know further, estemate or describe the problem in detail. Your current task is: \n[Task]\n This task is a subtask of the global task: [MasterTask]\n To accomplish this task, please review the following information: [PreText]\n[Agent] \nPlease complete this task.\n### Assistant:"
                }),
                "NextTaskPrompt": ("STRING", {
                    "multiline": True,
                    "default": "### Human: [CompletedTask]\n[SUMMARIZE]\nWhat would the optimal Task be to further complete the task? If you think the task is complete and no improvements can be made, generate a Task that includes the Text: 'FINISHED' (exactly the content inside ' ' all in capital letters).\n### Assistant: As your AGI Assistant, I have analyzed the Master Task and have identified the optimal approach to complete it. I believe the next step is to tackle the following task:\n"
                }),
                },
            "optional": {
                "Memory": ("NODE", {"input_format": {"node": "STRING"}}),
                "Tasks": ("NODE", {"input_format": {"node": "STRING"}}),
                "Agent": ("NODE", {"input_format": {"node": "STRING"}}),
            }
        }


    RETURN_TYPES = ("TEXT", "NODE")
    FUNCTION = "execute"
    CATEGORY = "Text"

    def execute(self, Master_Task, TextModel, Instructions, CompleteTaskPrompt, NextTaskPrompt, Log = [], Memory=None, Tasks=None, Agent=None):

        self.Master_Task = Master_Task.get("text", "")

        self.TextModel_save = TextModel
        self.TextModel_Master = TextModel.get("ModelNode", "")
        # print(TextModel_save)
        self.ModelNode, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed = self.TextModel_Master.split("||")
        class_obj = globals()[self.ModelNode]
        generate_text_Master = getattr(class_obj, "generate_text")

        LogTask = self.Master_Task
        try:
            LogTask_first = Log[0]
            LogTask_first = LogTask_first.get("Task", "")
        except:
            LogTask_first = LogTask
            self.Log = Log

        try:
            Last_Text = Log[-1]
            Last_Text = Last_Text.get("CompletedTask", "")
        except:
            Last_Text = "No additonal information is given"

        #CompleteTaskPrompt
        self.tokens_CompleteTaskPrompt = ["[Task]", "[MasterTask]", "[PreText]"]
        self.variables_CompleteTaskPrompt = [self.Master_Task, LogTask_first, Last_Text]

        if Agent != None:
            self.Agent = Agent.get("node", "")
            #print("Agent " + self.Agent)

            SaperateTokens2 = self.Agent.split("::")
            self.MasterAgentPrompt_combine = ""
            for SaperateToken2 in SaperateTokens2:
                self.CostumeAgent, self.CostumeToken, self.MasterAgentPrompt, self.AgentPrompt, self.AgentNextTaskPrompt, self.ModelNode, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed = SaperateToken2.split("||")
                self.MasterAgentPrompt_combine += self.MasterAgentPrompt +"\n"
                #print("MasterAgentPrompt_combine " + self.MasterAgentPrompt_combine)

            self.tokens_CompleteTaskPrompt = self.tokens_CompleteTaskPrompt + ["[Agent]"]
            self.variables_CompleteTaskPrompt = self.variables_CompleteTaskPrompt + [self.MasterAgentPrompt_combine]
        else:
            self.tokens_CompleteTaskPrompt = self.tokens_CompleteTaskPrompt + ["[Agent]"]
            self.variables_CompleteTaskPrompt = self.variables_CompleteTaskPrompt + [""]

        self.tokens_CompleteTaskPrompt_save = self.tokens_CompleteTaskPrompt
        self.variables_CompleteTaskPrompt_save = self.variables_CompleteTaskPrompt

        self.CompleteTaskPrompt = CompleteTaskPrompt
        for self.tokens_CompleteTaskPrompt, self.variables_CompleteTaskPrompt in zip(self.tokens_CompleteTaskPrompt, self.variables_CompleteTaskPrompt):
            self.CompleteTaskPrompt = self.CompleteTaskPrompt.replace(self.tokens_CompleteTaskPrompt, self.variables_CompleteTaskPrompt)

        print("____CompleteTaskPrompt____")
        print(self.CompleteTaskPrompt)


        self.CompletedTask = generate_text_Master(self, prompt = self.CompleteTaskPrompt, TextModel_g = self.TextModel_save)

        # #problems with repeat
        # RepeatToken1 = self.CompleteTaskPrompt[-10:]
        # if self.CompletedTask.find(RepeatToken1) != -1:  # if the token is found
        #     # extract the part of the string after the token
        #     self.CompletedTask = self.CompletedTask[self.CompletedTask.find(RepeatToken1) + len(RepeatToken1):]

        print("____CompletedTask____")
        print(self.CompletedTask)

        # NextTaskPrompt
        self.tokens_NextTaskPrompt = self.tokens_CompleteTaskPrompt_save + ["[CompletedTask]"]  # ["[Task]", "[MasterTask]", "[PreText]"]
        self.variables_NextTaskPrompt = self.variables_CompleteTaskPrompt_save + [self.CompletedTask + "/n"]  # [self.Master_Task, LogTask_first, Last_Text]

        if Agent != None:
            self.Agent_save = Agent
            self.Agent = Agent.get("node", "")
            # print("Agent " + self.Agent)

            SaperateTokens2 = self.Agent.split("::")
            self.MasterAgentPrompt_combine = ""

            for SaperateToken2 in SaperateTokens2:
                self.CostumeAgent, self.CostumeToken, self.MasterAgentPrompt, self.AgentPrompt, self.AgentNextTaskPrompt, self.ModelNode, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed = SaperateToken2.split("||")
                self.MasterAgentPrompt_combine += self.MasterAgentPrompt + "\n"
                # print("MasterAgentPrompt_combine " + self.MasterAgentPrompt_combine)

                class_obj = globals()[self.CostumeAgent]
                execute_Agent = getattr(class_obj, "execute")
                self.Agent_Answer, dummy = execute_Agent(self, self.CompletedTask, self.Agent_save)

                #schleife wie hier direct drunter: for self.tokens_NextTaskPrompt, self.variables_NextTaskPrompt in zip(self.tokens_NextTaskPrompt, self.variables_NextTaskPrompt):
                self.tokens_NextTaskPrompt = self.tokens_NextTaskPrompt + ["[" + self.CostumeToken + "]"]
                self.variables_NextTaskPrompt = self.variables_NextTaskPrompt + [self.Agent_Answer]


        self.NextTaskPrompt = NextTaskPrompt
        for self.tokens_NextTaskPrompt, self.variables_NextTaskPrompt in zip(self.tokens_NextTaskPrompt, self.variables_NextTaskPrompt):
            self.NextTaskPrompt = self.NextTaskPrompt.replace(self.tokens_NextTaskPrompt, self.variables_NextTaskPrompt)

        print("____NextTaskPrompt____")
        print(self.NextTaskPrompt)


        self.NextTask = generate_text_Master(self, prompt = self.NextTaskPrompt, TextModel_g = self.TextModel_save)

        # # problems with repeat
        # RepeatToken2 = self.NextTaskPrompt[-10:]
        # if self.NextTask.find(RepeatToken2) != -1:  # if the token is found
        #     # extract the part of the string after the token
        #     self.NextTask = self.NextTask[self.NextTask.find(RepeatToken2) + len(RepeatToken2):]

        print("____NextTask____")
        print(self.NextTask)

        Log.append({"CompleteTaskPrompt": self.CompleteTaskPrompt, "CompletedTask": self.CompletedTask, "NextTaskPrompt": self.NextTaskPrompt,"NextTask": self.NextTask, "Task": LogTask})

        #if len(Log) < 5: #specific number of passes
        if self.NextTask.find("FINISHED") == -1:
            log_string, dummy = CostumeMaster_1.execute(self, {"text": self.NextTask}, self.TextModel_save, Instructions, CompleteTaskPrompt, NextTaskPrompt, self.Log,  Memory, Tasks, Agent)
        else:
            log_string = ""
            for entry in Log:
                log_string += f"Complete Task Prompt:\n{entry['CompleteTaskPrompt']}\n\n"
                log_string += f"Completed Task:\n{entry['CompletedTask']}\n\n"
                log_string += f"Next Task Prompt:\n{entry['NextTaskPrompt']}\n\n"
                log_string += f"Next Task:\n{entry['NextTask']}\n\n"

            return ({"text": log_string}, self)
        log_string = log_string.get("text", "")
        return ({"text": log_string}, self)

class CostumeAgent_1:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "TextModelAgent1": ("TEXT_MODEL", {"input_format": {"ModelNode": "STRING"}}),
                "CostumeToken": ("STRING", {"default": "SUMMARIZE"}),
                "Instructions": ("STRING", {
                    "multiline": True,
                    "default": "Instructions:\nDo not write anything here!\nFirst input: Put in the first input the token which the master should say to start the agent.\nSecond input: Write a prompt that contains the token from the first input that gets inserted into the Token [Agent] in the master completion prompt. If you use multiple Agents they get pasted all among themselves\nThird input: Write a prompt that fulfills your needs. Include the [TEXT] token to input the last generated text\nWhen you combining two agents with the CombineInput node, make sure that the agents have different numbers, else i think it wont work\nIf you want more Agents you have to copy paste the CostumeAgent_1 class in the Textnode.py inside the costume node folder and change every number from 1 to the next number. Also include this inside the NODE_CLASS_MAPPINGS at the bottom."
                }),
                "MasterPrompt": ("STRING", {
                    "multiline": True,
                    "default": "You have the option to summarize by typing [SUMMARIZE] and than the thing you want to have summarized inside \{ \} brackets. For Example: [SUMMARIZE]\{the text to be summarized\}\n"
                }),
                "AgentPrompt": ("STRING", {
                    "multiline": True,
                    "default": "### Human: Please summarize the following text:\n[TEXT]\n### Assistant: Here is a summary of the Text:\n"
                }),
                "AgentNextTaskPrompt": ("STRING", {
                    "multiline": True,
                    "default": "Here is a Summary: [SUMMARIZE]"
                 })#,
                # "optional": {
                #     "Memory": ("NODE", {"input_format": {"node": "STRING"}}),
                #     "Tasks": ("NODE", {"input_format": {"node": "STRING"}}),
                #     "Agent": ("NODE", {"input_format": {"node": "STRING"}})
                # }
            }
        }


    RETURN_TYPES = ("NODE",)
    FUNCTION = "send"
    CATEGORY = "Text"

    def send(self, TextModelAgent1, CostumeToken, Instructions, MasterPrompt, AgentPrompt, AgentNextTaskPrompt):
        self.TextModelAgent1_Agent = TextModelAgent1.get("ModelNode", "")
        NodeAgent1 = "CostumeAgent_1||" + f"{CostumeToken}||{MasterPrompt}||{AgentPrompt}||{AgentNextTaskPrompt}||{self.TextModelAgent1_Agent}"
        #print("send")
        return ({"node": NodeAgent1}, self)

    def execute(self, AgentInputText, NodeAgent1):

        self.NodeAgent1_save = NodeAgent1
        self.NodeAgent1_Agent = NodeAgent1.get("node", "")
        # print(TextModel_save)
        self.CostumeAgent_1, self.CostumeToken, self.MasterPrompt, self.AgentPrompt, self.AgentNextTaskPrompt, self.ModelNode, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed = self.NodeAgent1_Agent.split("||")
        class_obj = globals()[self.ModelNode]
        generate_text_Agent = getattr(class_obj, "generate_text")

        ModelNode_Agent =f"{self.ModelNode}||{model_name}||{max_new_tokens}||{temperature}||{top_p}||{typical_p}||{repetition_penalty}||{encoder_repetition_penalty}||{top_k}||{min_length}||{no_repeat_ngram_size}||{num_beams}||{penalty_alpha}||{length_penalty}||{seed}"
        self.TextModelAgent1_Model = {"ModelNode": ModelNode_Agent} #???

        #self.AgentPrompt = AgentInputText und self.AgentPrompt
        #find [TEXT]
        #replace text with [TEXT] with output
        try:
            self.start_index = AgentInputText.index("[" + self.CostumeToken + "]") + len("[" + self.CostumeToken + "]")
            self.AgentInputText = AgentInputText.index("\}", self.start_index)
            self.AgentPrompt = self.self.AgentPrompt.replace([TEXT], self.AgentInputText)
            print("____AgentPrompt____")
            print(self.AgentPrompt)

            self.AgentText = generate_text_Agent(self, prompt=self.self.AgentPrompt, TextModel_g=self.TextModelAgent1_Model)

            self.AgentText = self.AgentNextTaskPrompt.replace("[" + self.CostumeToken + "]", self.AgentText)

        except:
            print("\nMissing Token, Brackets [] or {} of the Completed Task. No agent prompt . Returning: Agent failed. Probably cause is missing or misspelled token or missing Brackets like [] or {}\n")
            self.AgentText = "Agent failed. Probably cause is missing or misspelled token or missing Brackets like [] or \{\}"

        return (self.AgentText , self)

class CostumeAgent_2:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "TextModelAgent2": ("TEXT_MODEL", {"input_format": {"ModelNode": "STRING"}}),
                "CostumeToken": ("STRING", {"default": "SUMMARIZE"}),
                "Instructions": ("STRING", {
                    "multiline": True,
                    "default": "Instructions:\nDo not write anything here!\nFirst input: Put in the first input the token which the master should say to start the agent.\nSecond input: Write a prompt that contains the token from the first input that gets inserted into the Token [Agent] in the master completion prompt. If you use multiple Agents they get pasted all among themselves\nThird input: Write a prompt that fulfills your needs. Include the [TEXT] token to input the last generated text\nWhen you combining two agents with the CombineInput node, make sure that the agents have different numbers, else i think it wont work\nIf you want more Agents you have to copy paste the CostumeAgent_1 class in the Textnode.py inside the costume node folder and change every number from 1 to the next number. Also include this inside the NODE_CLASS_MAPPINGS at the bottom."
                }),
                "MasterPrompt": ("STRING", {
                    "multiline": True,
                    "default": "You have the option to summarize by typing [SUMMARIZE]"
                }),
                "AgentPrompt": ("STRING", {
                    "multiline": True,
                    "default": "### Human: Please summarize the following text:\n[TEXT]\n### Assistant: Here is a summary of the Text:\n"
                }),
                "AgentNextTaskPrompt": ("STRING", {
                    "multiline": True,
                    "default": "Here is a Summary: [SUMMARIZE]"
                 })#,
                # "optional": {
                #     "Memory": ("NODE", {"input_format": {"node": "STRING"}}),
                #     "Tasks": ("NODE", {"input_format": {"node": "STRING"}}),
                #     "Agent": ("NODE", {"input_format": {"node": "STRING"}})
                # }
            }
        }


    RETURN_TYPES = ("NODE",)
    FUNCTION = "send"
    CATEGORY = "Text"

    def send(self, TextModelAgent2, CostumeToken, Instructions, MasterPrompt, AgentPrompt, AgentNextTaskPrompt):
        self.TextModelAgent2_Agent = TextModelAgent2.get("ModelNode", "")
        NodeAgent2 = "CostumeAgent_2||" + f"{CostumeToken}||{MasterPrompt}||{AgentPrompt}||{AgentNextTaskPrompt}||{self.TextModelAgent2_Agent}"
        #print("send")
        return ({"node": NodeAgent2}, self)

    def execute(self, AgentInputText, NodeAgent2):

        self.NodeAgent2_save = NodeAgent2
        self.NodeAgent2_Agent = NodeAgent2.get("ModelNode", "")
        # print(TextModel_save)
        self.CostumeAgent_2, self.CostumeToken, self.MasterPrompt, self.AgentPrompt, self.AgentNextTaskPrompt, self.ModelNode, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed = self.NodeAgent2_Agent.split("||")
        class_obj = globals()[self.ModelNode]
        generate_text_Agent = getattr(class_obj, "generate_text")

        ModelNode_Agent =f"{self.ModelNode}||{model_name}||{max_new_tokens}||{temperature}||{top_p}||{typical_p}||{repetition_penalty}||{encoder_repetition_penalty}||{top_k}||{min_length}||{no_repeat_ngram_size}||{num_beams}||{penalty_alpha}||{length_penalty}||{seed}"
        self.TextModelAgent2_Model = {"ModelNode": ModelNode_Agent} #???

        #self.AgentPrompt = AgentInputText und self.AgentPrompt
        #find [TEXT]
        #replace text with [TEXT] with output
        self.AgentInputText = AgentInputText
        self.AgentPrompt = self.self.AgentPrompt.replace([TEXT], self.AgentInputText)

        self.AgentText = generate_text_Agent(self, prompt=self.self.AgentPrompt, TextModel_g=self.TextModelAgent2_Model)


        log_string = log_string.get("text", "")
        return ({"text": log_string}, self)

class CombineInput:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input1": ("NODE", {"input_format": {"node": "STRING"}}),
                "Input2": ("NODE", {"input_format": {"node": "STRING"}})
            }
        }

    RETURN_TYPES = ("NODE",)
    FUNCTION = "combine"
    CATEGORY = "Text"

    def combine(self, Input1, Input2):
        Input1 = Input1.get("node", "")
        #print("Input1 " + Input1)
        self.Identify1, self.CostumeToken1, self.MasterAgentPrompt1, self.AgentPrompt1, self.ModelNode, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed = Input1.split("||")
        Input2 = Input2.get("node", "")
        #print("Input2 " + Input2)
        self.Identify2, self.CostumeToken2, self.MasterAgentPrompt2, self.AgentPrompt2, self.ModelNode, model_name, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed = Input2.split("||")
        if (self.Identify1.find("CostumeAgent") != -1) & (self.Identify2.find("CostumeAgent") != -1):
            Output = Input1 + "::" + Input2
            #print("Output " + Output)
        else:
            print("Error in combining")
            Output = None
        return ({"node": Output}, self)


# A dictionary that contains all nodes you want to export with their names
NODE_CLASS_MAPPINGS = {
    "TextInput": TextInput,
    "TextOutput": TextOutput,
    "TextGenerator": TextGenerator,
    "TextCombine": TextCombine,
    "Image_generation_Conditioning": Image_generation_Conditioning,
    "CostumeMaster_1": CostumeMaster_1,
    "CostumeAgent_1": CostumeAgent_1,
    "CostumeAgent_2": CostumeAgent_2,
    "Model_1": Model_1,
    "Memory_Excel": Memory_Excel,
    "CombineInput": CombineInput,
    
    
}
