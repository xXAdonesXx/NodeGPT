# NodeGPT
ComfyUI Extension Nodes for Automated Text Generation.

For now, this is only a start. The goal is to build a node-based Automated Text Generation AGI. This extension should ultimately combine the powers of, for example, AutoGPT, babyAGI, and Jarvis. I think the advantage of a node-based system is that non-programmers can try out different ideas, and, for example, memory nodes with diffrent structurs can be replaced easily.

![Screenshot 2023-04-08 183920](https://user-images.githubusercontent.com/66518617/230733165-7c7d71bc-9141-4a86-9d22-94c2885f6208.png)

# Example of Agents 

You can make your own costume agents with the costume nodes! 

Master Instructions:
First input: Write your completion prompt similar to the example. You should definitely include [Task]
Second input: Write your nexttask prompt similar to the example. You should definitely include [CompletedTask] and Tell it to say FINISHED if its finished with the global task. This will break the loop, if its included in the next task
Write your Prompt and include the Tokens formatted like this [Token]. The tokens getting replaced by the corresponding text.
Please not include || or ::or quotation marks other than ' in your Prompts!
Tokens: [Task] = the current task (should be in The prompt); [MasterTask] = Your overall goal (input); [PreText] = Previous generated completed task; [Memory] = to do; [Tasks] = to do; [Agent] = all Agent Prompts;
Please write an feature request on Github if you think any Token is missing.

Agent Instructions:
First input: Put in the first input the token which the master should say to start the agent.
Second input: Write a prompt that contains the token from the first input that gets inserted into the Token [Agent] in the master completion prompt. If you use multiple Agents they get pasted all among themselves
Third input: Write a prompt that fulfills your needs. Include the [TEXT] token to input the last generated text
When you combining two agents with the CombineInput node, make sure that the agents have different numbers, else i think it wont work
If you want more Agents you have to copy paste the CostumeAgent_1 class in the Textnode.py inside the costume node folder and change every number from 1 to the next number. Also include this inside the NODE_CLASS_MAPPINGS at the bottom.

![grafik](https://user-images.githubusercontent.com/66518617/234352468-2982ab25-e4d8-4b4e-8a5e-390be26781cf.png)

The CostuemAgent is not fully tested, because my prompt skills are to bad to get an output that the agent can use.

# Features
- Text generation inside ComfyUI with LLaMA-like vicuna-13b-4bit-128g and gpt4-x-alpaca-13b-native-4bit-128g

- GPT-Master and GPT-Agents

- Stable Diffusion Prompt enhancement (not tested yet due to low VRAM requirements)

# Possible Features
- GPT4 API support

- Memory node (prtially finished)

- Task queue (kind of there)

- Different tasks like browsing the web or executing code or image recognition

something like this:

![FsW_uXMaEAAWaX0](https://user-images.githubusercontent.com/66518617/230734768-6a1ed138-09d3-41d9-85cf-b4107cf00cbe.jpeg)
https://github.com/yoheinakajima/babyagi

# Installing
Install: https://github.com/comfyanonymous/ComfyUI

Install: https://github.com/oobabooga/text-generation-webui

Download the Textnode.py file and move it into the costume_nodes folder ...\ComfyUI\custom_nodes

Use "python server.py --auto-devices --listen --no-stream --model vicuna-13b-4bit-128g --wbits 4 --groupsize 128 --model_type llama" or just "python server.py --auto-devices --listen --no-stream" to start the text-generation-webui

Start ComfUI to place nodes and enjoy

# Contributing
Pull requests, suggestions, and issue reports are welcome.

Before reporting a bug, make sure that you have:

1. Created a conda environment and installed the dependencies exactly as in the Installation section above.

2. Searched to see if an issue already exists for the issue you encountered.

# Credits
ComfyUI: https://github.com/comfyanonymous/ComfyUI

oobabooga: https://github.com/oobabooga/text-generation-webui

chatGPT: https://chat.openai.com/chat
