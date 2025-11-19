import gradio as gr
import requests

OLLAMA_URL = "http://localhost:11434/v1/chat/completions"
MAX_HISTORY = 6

def chat_lumora(user_input, previous_context):
    messages = previous_context[-MAX_HISTORY:]
    messages.append({"role": "user", "content": user_input})
    
    data = {"model": "lumora", "messages": messages}
    
    try:
        response = requests.post(OLLAMA_URL, json=data, timeout=50)
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        answer = f"Fehler bei der Verbindung zu Ollama: {e}"
    
    previous_context.append({"role": "user", "content": user_input})
    previous_context.append({"role": "assistant", "content": answer})
    
    return answer, previous_context, ""

context = []

with gr.Blocks(css="""
    textarea, .gr-textbox {
        font-size: 18px !important;
    }
    .gr-button {
        font-size: 16px !important;
    }
    .gr-textbox[readonly] {
        font-size: 18px !important;
    }
""") as demo:
    gr.Markdown("<h2 style='text-align:center; color:#2E86C1;'>Lumora – Dein KI-Begleiter</h2>")
    gr.Markdown("<p style='text-align:center'>Ruhige, strukturierte Unterstützung für Alltag, Fokus und Planung.</p>")

    # Eingabefeld
    chatbox = gr.Textbox(
        label="Deine Frage / Nachricht",
        placeholder="Hier tippen... (Enter = neue Zeile, Shift+Enter = senden)",
        lines=3
    )

    # Antwortfeld
    chat_output = gr.Textbox(
        label="Lumora antwortet:",
        interactive=False,
        lines=10,
        max_lines=30,
        placeholder="Antwort erscheint hier..."
    )

    state = gr.State(value=[])

    # Button
    send_btn = gr.Button("Senden")
    send_btn.click(chat_lumora, inputs=[chatbox, state], outputs=[chat_output, state, chatbox])
    
    # Enter → senden
    chatbox.submit(chat_lumora, inputs=[chatbox, state], outputs=[chat_output, state, chatbox])

    # JS für Shift+Enter / Enter Verhalten
    gr.HTML("""
    <script>
    const textarea = document.querySelector('textarea');
    if (textarea) {
        textarea.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const btn = document.querySelector('button');
                if (btn) btn.click();
            }
        });
    }
    </script>
    """)

demo.launch(server_name="127.0.0.1", server_port=7860)

