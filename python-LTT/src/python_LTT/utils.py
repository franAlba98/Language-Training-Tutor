import ollama


def do_something_useful():
    print("Replace this with a utility function")


def call_ollama(prompt: str, model: str = "llama3") -> str:
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]