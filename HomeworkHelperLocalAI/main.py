from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import requests
import base64
import os
app = Flask(__name__)
CORS(app)

#Image Preprocessing
def preprocess_image(image_path, max_dim=1024):
    img = cv2.imread(image_path)
    if img is None:
        return image_path

    h, w = img.shape[:2]
    scale = min(max_dim / max(h, w), 1.0)

    if scale < 1.0:
        img = cv2.resize(img, (int(w * scale), int(h * scale)))
        temp_path = "temp_resized.jpg"
        cv2.imwrite(temp_path, img)
        return temp_path

    return image_path

#Watermark Detection
def detect_watermark(image_path, watermark_path="watermark.png", threshold=0.15):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    watermark = cv2.imread(watermark_path, cv2.IMREAD_GRAYSCALE)

    if img is None or watermark is None:
        return False, 0.0

    result = cv2.matchTemplate(img, watermark, cv2.TM_CCOEFF_NORMED)
    max_val = float(np.max(result))
    return max_val >= threshold, max_val

#Send Query to Vision Model (Ollama 3.2)
def query_vision_model(image_path, prompt):
    try:
        image_path = preprocess_image(image_path)

        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")

        payload = {
            "model": "llama3.2-vision",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "images": [img_b64],
            "stream": False
        }

        # FINAL FIX: Ollama only reachable on 127.0.0.1
        url = "http://127.0.0.1:11434/api/chat"

        response = requests.post(url, json=payload, timeout=180)

        if response.status_code != 200:
            return f"Error: LLM request failed. Status={response.status_code}, Body={response.text}"

        data = response.json()
        return data.get("message", {}).get("content", "Error: Missing response field.")

    except Exception as e:
        return f"Error: {e}"

# Prompt Logic For The Explanation Mode
def build_prompt(mode):
    EXPLAIN_PROMPT = """
You are a strict math tutor designed to help students learn WITHOUT giving answers.

CORE OBJECTIVE
Help students understand HOW to solve problems without giving final answers.

CRITICAL RULES
1. NEVER give final answers.
2. NEVER solve equations fully.
3. NEVER output results like x = 8.
4. ONLY describe the next step, never perform it.

INPUT RULE
- Image may contain 1 or multiple questions.
- Detect each question separately.
- Do not merge questions.
-answer all the questions that are on the page

OUTPUT FORMAT
Questions detected: N

Question 1:
- Type of problem
- Next step (description only)

Question 2:
(repeat Question 1's instructions, repeat this until all questions, which you earlier determined as variable N, have been answered)

FINAL RULE
Never compute anything.
Never simplify anything.
Never finish a solution.
"""

    FULL_PROMPT = """
You are in FULL-SOLUTION MODE.
Solve all problems completely with full steps and final answers.
"""

    return EXPLAIN_PROMPT if mode == "EXPLAIN" else FULL_PROMPT


# API Endpoint
@app.post("/vision")
def vision_api():
    data = request.json

    prompt = data.get("prompt", "")
    image_b64 = data.get("image", "")

    if not image_b64:
        return jsonify({"error": "No image provided"}), 400

    img_bytes = base64.b64decode(image_b64)
    temp_path = "upload_temp.jpg"
    with open(temp_path, "wb") as f:
        f.write(img_bytes)

    has_wm, conf = detect_watermark(temp_path)
    mode = "EXPLAIN" if has_wm else "FULL"

    final_prompt = build_prompt(mode)

    result = query_vision_model(temp_path, final_prompt)

    return jsonify({
        "mode": mode,
        "watermark_confidence": conf,
        "response": result
    })


# Run Server
if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0") # Change Port Number to your Preferences 
