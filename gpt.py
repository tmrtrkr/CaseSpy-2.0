import openai
import threading

class Generator:
    @staticmethod
    def generate(prompts, model_choice, gpt_api_key, grok_api_key):
        if model_choice == 2:  # GPT
            return Generator.query_gpt(prompts[0], gpt_api_key)
        else:  # Grok (default)
            return Generator.query_grok(prompts[0], grok_api_key)

    @staticmethod
    def query_grok(text, api_key):
        client = openai.OpenAI(
            base_url="https://api.x.ai/v1",
            api_key=api_key,
        )
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text},
        ]
        try:
            completion = client.chat.completions.create(
                model="grok-3",
                messages=messages,
                temperature=0.7,
                timeout=30
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Grok API hatası: {e}"

    @staticmethod
    def query_gpt(text, api_key):
        openai.api_key = api_key
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": text}
                ],
                temperature=0.7,
                max_tokens=600,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            print("HTTP 200")
            return response.choices[0].message.content
        except Exception as e:
            return f"GPT API hatası: {e}"

def send_prompt(Prompt, gpt_api_key, grok_api_key, model_choice=1):  # Default to Grok (1)
    return Generator.generate([Prompt], model_choice, gpt_api_key, grok_api_key)