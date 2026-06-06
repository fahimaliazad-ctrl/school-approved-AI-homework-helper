document.getElementById("send").onclick = async () => {
  const chat = document.getElementById("chat");
  const prompt = document.getElementById("prompt").value;
  const file = document.getElementById("imageInput").files[0];

  if (!file) {
    chat.innerHTML += "\n[Error] No image selected.";
    return;
  }

  // Convert image → base64
  const base64 = await new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result.split(",")[1]);
    reader.readAsDataURL(file);
  });

  chat.innerHTML += `\nYou: ${prompt}`;

  const response = await fetch("http://192.168.1.185:5000/vision", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      prompt: prompt,
      image: base64
    })
  });

  const data = await response.json();

  chat.innerHTML += `\n[Mode: ${data.mode}]`;
  chat.innerHTML += `\nAI: ${data.response}`;
};
