# Discord LM Studio Base example
Minimal Discord bot (utilizes [Pycord](https://pycord.dev/)) that watches a Discord channel, and responds accordingly to every message. It utilizes a server being ran by a local LM Studio instance to serve as the bot's brains

#### Note
I slightly stress tested it with multiple users talking to it at once, but can't guarantee stability. Seemed to work fine for me tho

## What I run
I was utilizing [EnlistedGhost/Ministral-3-14B-Instruct-2512-GGUF](https://huggingface.co/EnlistedGhost/Ministral-3-14B-Instruct-2512-GGUF) with quant Q6_K for my test case. I am using a custom prompt to make it act like "a chill, slightly toxic Gen Z guy in a Discord chat. You are NOT an AI. You are a real person." I will not be sharing my prompt due for a couple of reasons ;)

#### Ministral parameters
*Note: Only gonna show changes I personally made*
* Context Length: `8192`
* Prompt Template (Manual)
    * Before System: `<s>`
    * After System: `\n\n`
    * Before User: `[INST] ` note the space after
    * After User: ` [/INST]` not the space before
    * Before Assistant: ` ` single space
    * After Assistance: `</s>`
    * Disabled Reasoning Section Parsing
* Temperature: `0.7`
* Top P Sampling: `0.9`

## How To Use
The sample code gives basically everything you need to get a simple chat bot up and running. The bot is programmed to watch a channel, and respond whenever it sees a message. There are some changes you will need to make to get it running. You will also need LM Studio installed, and need a local server instance running under the Developer tab for the bot to connect to.

### Modifying Variables
If you look inside `.env.example`, you will see how you should set up your environment variables. I kept it simple and left everything you will need to modify in here (lazy to also include json lmao). You will just need to rename that file to just `.env`, and modify the variables that works for you.

#### Knowing how to modify variables
Your setup may not match mine exactly, so you will need to modify some things. Depending on your hardware configuration, you may need or want to use a different model, or need a smaller chat history. You will need to change the model and chat limit accordingly. I can't help you with getting the best setup for your use case, you will need to figure that stuff out on your own 😽 There are multiple guides for figuring out what works best for you, including this [guide on geeksforgeeks](https://www.geeksforgeeks.org/deep-learning/recommended-hardware-for-running-llms-locally/).

You will also need to know how to modify the model's settings and use a good prompt to satisfy your needs. Just throwing in a random model without any modification will most likely yield disappointing results. Once again though, I will not help you with that 😽 you can figure that out on your own

When in doubt, you could always bother some online AI model lol

#### Tested on
Windows 11 24H2, LM Studio `0.3.36`, CUDA/CPU llama.cpp (Windows) `v1.66.0 stable`, py-cord `2.7.0`