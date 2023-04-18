# NodeGPT
ComfyUI Extension Nodes for Automated Text Generation.

For now, this is only a start. The goal is to build a node-based Automated Text Generation AGI. This extension should ultimately combine the powers of, for example, AutoGPT, babyAGI, and Jarvis. I think the advantage of a node-based system is that non-programmers can try out different ideas, and, for example, memory nodes with diffrent structurs can be replaced easily.

![Screenshot 2023-04-08 183920](https://user-images.githubusercontent.com/66518617/230733165-7c7d71bc-9141-4a86-9d22-94c2885f6208.png)

# Example of MasterAgent_Test

Example of the MasterAgent_Test node with the input "give me instructions for the construction of a house". Used the gpt4-x-alpaca-13b-native-4bit-128g model.
The Output is visible in the command prompt.
Please note that this is far perfect and has a lot of room for improvements. While it can be enjoyable and worthwhile, there may be ways to enhance or optimize the experience. 

![give me instructions for the construction of a house](https://user-images.githubusercontent.com/66518617/232895426-545343ce-a133-4ceb-b39b-75293b40cafa.png)

*Completed Task*

 Building a House - Step-by-Step Instructions
1. Research local building regulations and obtain necessary permits.2. Clear and level the building site.3. Excavate the foundation and pour concrete.4. Frame the walls with floor joists and roof rafters.5. Install exterior finishes like siding and windows.6. Lay out and install interior finish materials, such as drywall and flooring.7. Connect all electrical wiring and fixtures.8. Plumb and hook up water lines and sewer systems.9. Finish landscaping and outdoor areas.10. Final inspections and touch-ups.


*Next Task*

 Further refine the instructions and provide more detailed information on specific steps, including but not limited to: a) design considerations, b) material selection, c) construction techniques, d) safety measures, e) budget management, and f) potential challenges and their solutions.


*Completed Task*

 As an AI assistant, I am unable to perform physical actions such a clearing a building or installing electical wires. However, for each step listed, if you provide specific details or questions related to that step, i can assist you in providing information, guidance or estimation.


*Next Task*

 'Generate a comprehensive list of essential materials needed for building a home, categorized by phase of construction and specific tasks.'
This will provide a valuable resource for anyone looking to build a new home or undertake renovation projects.


*Completed Task*

 Phase 1 - Foundation and Excavation:
1. Obtain necessary permits and approvals from local authorities.2. Clear and level the building site, removing trees and vegetation.3. Dig a foundation trench and pour a concrete foundation.4. Install footings and anchor bolts.5. Lay waterproofing membranes and exterior insulation.6. Compact the soil and grade the land.7. Place steel reinforcement bars and concrete slabs for walls and columns.8. Build retaining walls, as required.Phase II - Walls and Roof:10. Construct wall forms and poured concrete walls.11, Install windows and doors, and seal air leaks.  Photos of completed tasks would be appreciated.


*Next Task*

 'Generating a Comprehensive List of Essential Materials Needed for Building a Home, Categorized By Phases of Construction and Specific Tasks'.
Please provide any relevant details, questions or context for this sub-task, so I can provide the most accurate and helpful information possible.


*Completed Task*

 Here is the list of essential materials needed for building a home, categorized by phases of construction and specific tasks:Phases:• Foundation & Exavtion: - Obtai...


*Next Task*

 'Categorize the essential building materials into different groups based on their functions and tasks during construction.'This task will further refine the information provided and make it easier for you to understand the different material categories and their roles in the construction process.Once again, if you want to finalize this particular task and mark it as completed, you can generate the Task 'CATEGORIZING_MATERIALS_FUNCTIONS' with the text 'Finished' inside the '...' marks.


*Completed Task*

 Categorizing the building material...


# Features
- Text generation inside ComfyUI with LLaMA-like vicuna-13b-4bit-128g and gpt4-x-alpaca-13b-native-4bit-128g

- Stable Diffusion Prompt enhancement (not tested yet due to low VRAM requirements)

- Mini GPT-Agent

# Possible Features
- GPT4 API support

- GPT-Agents nodes

- Memory node (prtially finished)

- Task queue

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
