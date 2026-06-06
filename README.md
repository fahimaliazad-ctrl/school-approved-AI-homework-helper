# school-approved-AI-homework-helper
A simple setup for running Ollama on my Mac mini and letting any other device on your Wi‑Fi use it like a shared server. made as a PoC for schools that could implement it so everything just sends requests to one machine. this allows for schools to moderate AI use. The repo includes the config, example API calls, and a tiny front‑end.

## Problem

Schools are unsure how to handle AI in education. AI is useful for learning, but allowing every student to use public AI services isn't feasible due to restrictions on privacy and lack of oversight.

## Solution

This project uses a Flask server and locally-hosted AI models through Ollama to provide AI assistance over a school network.

If this proof of concept were scaled up (the 3.2B model I used was due to the constraints of my hardware), students would be able to access an AI service the school runs locally. Students connect through a web interface and send requests to the server, which generates responses using local AI models.

On the topic of the hardware, I am aware that there is an upfront cost associated with running capable models effectively. However, I believe this is a reasonable investment for schools to look into in exchange for the control of AI use and privacy concerns.

## Why I Built This

I'm on a board of student advisors to my school's superintendent and an officer at my school's AI club, so naturally the topic of AI comes up often. A major concern I heard is the abuse of AI affecting academic integrity, and this concern led to our school blocking most AI websites. I did some research, and I realized a locally-hosted server could provide AI access for an entire school while maintaining greater control over deployment.

## Architecture

The application uses a simple client-server architecture.

User Browser  
↓  
Flask  
↓  
Ollama  
↓  
Local AI Model  

### Request Flow

1. A user submits a prompt or uploads an image through the web interface.
2. The frontend sends the request to a Flask endpoint.
3. Flask processes the request by:
   - Detecting watermarks
   - Selecting the appropriate mode
   - Building the model prompt
   - Preparing image data when needed
4. Flask sends the request to Ollama through the local API.
5. Ollama runs the selected model and returns a response.
6. Flask returns the result to the frontend.

### Image Processing

For image uploads:

- The frontend sends the image to Flask.
- Flask temporarily processes and encodes the image.
- The image is sent to Ollama's vision model.
- The generated response is returned to the user.

### Privacy

All processing occurs locally.

- No cloud AI services are used.
- No conversation history is stored.
- No prompts or images are permanently saved.

Each request is processed independently and discarded after completion.

## Features

- Locally-hosted AI models
- Browser-based interface
- Vision model support
- Multi-device access
- Centralized deployment
- No cloud API costs
- School-controlled infrastructure

## Results

The system successfully demonstrates that a single computer can host AI models and provide responses to multiple users over a local network.

The project serves as a proof-of-concept for how schools could deploy AI infrastructure while maintaining greater control over privacy, costs, and system configuration.

## First‑Time Setup Guide

Follow these steps to run the program locally on your own computer.

---

## 1. Install Required Software

### Install Python 3.10+
https://www.python.org/downloads/

### Install Git
https://git-scm.com/downloads

### Install Ollama
https://ollama.com

---

## 2. Clone the Repository

```bash
git clone https://github.com/<your-username>/HomeworkHelperLocalAI.git
cd HomeworkHelperLocalAI
```

---

## 3. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows users:

```bash
venv\Scripts\activate
```

---

## 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Install the Vision Model in Ollama

```bash
ollama pull llama3.2-vision
```

Note: The program uses the `llama3.2-vision` model.  
This model is intentionally lightweight (3.2 billion parameters), which makes it easy to run on most machines.  
However, its reasoning ability is limited. Larger models (13B, 30B, 70B) can be swapped in later without changing the program’s code.

---

## 6. Start the Ollama Server

Open a new terminal window and run:

```bash
export OLLAMA_HOST=0.0.0.0:11434
ollama serve
```

You should see:

```
Listening on [::]:11434
```

Leave this terminal open.

---

## 7. Start the Backend (Flask API)

In the original terminal (with the virtual environment active):

```bash
python3 main.py
```

The backend will run at:

```
http://0.0.0.0:5000
```

---

## 8. Start the Frontend

Open another terminal:

```bash
cd test-site
python3 -m http.server 8000
```

The frontend will run at:

```
http://localhost:8000
```

---

## 9. Using the Program

1. Open the frontend in your browser.  
2. Upload a homework image.  
3. The program will:
   - preprocess the image  
   - detect watermarks  
   - choose Explain Mode or Full Solution Mode  
   - send the image and prompt to the local vision model  
4. The model returns the explanation or solution.

---

## Troubleshooting

### Error: model not found
Run:
```bash
ollama pull llama3.2-vision
```

### Error: connection refused
Check the following:
- `ollama serve` is running  
- You are connecting to `127.0.0.1:11434`  
- No Ollama GUI process is blocking the port  

### Explanations are low quality
This is expected with a 3.2B model.  
Use a larger model for stronger reasoning.

---

## Completed Setup

The program should now be fully operational on your machine.

