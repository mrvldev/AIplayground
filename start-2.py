import ollama

response = ollama.list()

res = ollama.chat(
    model="lumora",
    messages=[
        {"role": "user", "content": "Warum ist da Meer so salzig?"
         },
         ],
         stream=True
)
print(response)
for chunk in res:
    print(chunk["message"]["content"], end="", flush=True)