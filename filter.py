# filter.py — UPDATED
from groq import Groq
from config import GROQ_API_KEY

groq_client = Groq(api_key=GROQ_API_KEY)

def is_positive_with_groq(title: str, description: str) -> bool:
    content = f"Title: {title}\nDescription: {description}".strip()[:1000]
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a positivity detector. Respond ONLY 'Yes' or 'No'. "
                        "Say 'Yes' if content shows kindness, hope, rescue, success, joy, "
                        "community help, inspiration, or good news. Ignore neutral/negative."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Is this positive?\n\n{content}",
                }
            ],
            # 🔥 REPLACED DECOMMISSIONED MODEL
            model="llama-3.1-8b-instant",  # ← THIS IS THE FIX
            temperature=0.1,
            max_tokens=5,
        )
        return "yes" in chat_completion.choices[0].message.content.lower()
    except Exception as e:
        print(f"⚠️ Groq error: {e}")
        return is_positive_fallback(title, description)

def is_positive_fallback(title, description):
    text = (title + " " + description).lower()
    positive_words = ['success', 'happy', 'hope', 'kindness', 'rescue', 'inspire', 'good news']
    negative_words = ['death', 'accident', 'crime', 'scam']
    if any(w in text for w in negative_words):
        return False
    return any(w in text for w in positive_words)