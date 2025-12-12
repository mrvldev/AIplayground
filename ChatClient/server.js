import express from "express";
import cors from "cors";
import fetch from "node-fetch";

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static("public")); // dient index.html aus

// -------------------------------------------
// Ollama Anfrage (Zeilenweise JSON parsen)
// -------------------------------------------
async function askOllama(prompt) {
  const res = await fetch("http://localhost:11434/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "lumora",
      prompt,
      stream: true
    })
  });

  const text = await res.text();
  let fullResponse = "";

  for (const line of text.split("\n")) {
    if (!line.trim()) continue;
    try {
      const obj = JSON.parse(line);
      if (obj.response) fullResponse += obj.response;
    } catch (e) {
      // unvollständige JSON-Zeilen ignorieren
    }
  }

  return fullResponse;
}

// -------------------------------------------
// Chat API Endpoint
// -------------------------------------------
app.post("/api/chat", async (req, res) => {
  try {
    const userMessage = req.body.message || "";
    const reply = await askOllama(
      `Der Nutzer sagt: "${userMessage}". Antworte freundlich und hilfreich.`
    );
    res.json({ response: reply });
  } catch (err) {
    console.error("Fehler bei Ollama:", err);
    res.status(500).json({ error: "Ollama antwortet nicht" });
  }
});

// -------------------------------------------
// Server starten
// -------------------------------------------
const PORT = 3000;
app.listen(PORT, () => console.log(`Server läuft auf http://localhost:${PORT}`));

