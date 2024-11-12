# Gemini: AIzaSyBNEfVTO1k68YZmj6UYjrjA2r14la59da8
# OpenAI: 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

from openai import OpenAI

client = OpenAI(
    api_key="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"
)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about recursion in programming."},
    ],
)

print(completion.choices[0].message)
