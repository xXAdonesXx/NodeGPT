# NodeGPT
ComfyUI Extension Nodes for Automated Text Generation.

For now, this is only a start. The goal is to build a node-based Automated Text Generation AGI. This extension should ultimately combine the powers of, for example, AutoGPT, babyAGI, and Jarvis. I think the advantage of a node-based system is that non-programmers can try out different ideas, and, for example, memory nodes with diffrent structurs can be replaced easily.

![Screenshot 2023-04-08 183920](https://user-images.githubusercontent.com/66518617/230733165-7c7d71bc-9141-4a86-9d22-94c2885f6208.png)

# Features
- For now, only text generation inside ComfyUI with LLaMA-like vicuna-13b-4bit-128g

- Stable Diffusion Prompt enhancement (not tested yet due to low VRAM requirements)

# Possible Features
- GPT4 API support

- GPT-Agents nodes

- Memory node

- Task queue

- Different tasks like browsing the web or executing code or image recognition

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
