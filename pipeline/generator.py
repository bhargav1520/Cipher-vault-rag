import ollama
from config import OLLAMA_MODEL


def generate_answer(query: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)
    prompt = (
        "Answer the question directly and concisely, using only the facts "
        "in the context below. If a specific number, name, or fact is present "
        "in the context, state it plainly. If the context does not contain "
        "the answer, say so in one sentence — do not guess or hedge.\n\n"
        f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    )
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]
