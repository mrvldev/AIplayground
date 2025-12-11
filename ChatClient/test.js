import fetch from "node-fetch";

async function testOllama() {
  const res = await fetch("http://localhost:11434/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "llama3.1",
      prompt: "Sag Hallo!",
      stream: true
    })
  });

  const text = await res.text();  // Entire response as text
  let fullResponse = "";

  for (const line of text.split("\n")) {
    if (!line.trim()) continue;
    try {
      const obj = JSON.parse(line);
      if (obj.response) fullResponse += obj.response;
    } catch (e) {
      // ignore incomplete JSON fragments
    }
  }

  console.log("Antwort von Ollama:", fullResponse);
}

testOllama();
