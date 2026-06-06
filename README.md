# school-approved-AI-homework-helper
A simple setup for running Ollama on my Mac mini and letting any other device on your Wi‑Fi use it like a shared server. made as a PoC for schools that could implement it so everything just sends requests to one machine. this allows for schools to moderate AI use. The repo includes the config, example API calls, and a tiny front‑end.

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

