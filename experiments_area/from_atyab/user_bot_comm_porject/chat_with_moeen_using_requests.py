import os
import requests

from dotenv import load_dotenv

load_dotenv()


def main():
    # This accepts a POST request with data involving API key, User Message, Model Info & Model Config
    OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    request_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    user_input = input("What do you want to ask ? (or type exit): ")

    request_body = {
        "model": "gpt-4.1-mini",
        "messages": [{"role": "user", "content": user_input}],
        "temperature": 0.5,
    }

    response = requests.post(OPENAI_API_URL, headers=request_headers, json=request_body)
    result_dict = response.json()

    print(result_dict.get("choices")[0].get("message").get("content"))

    """
  {'id': 'chatcmpl-EYQ5ymXTC3rXFkTTR3Fz9C2VoOrg6', 'object': 'chat.completion', 
  'created': 1791872170, 'model': 'gpt-4.1-mini-2025-04-14', 
  'choices': [
    {'index': 0, 'message': {'role': 'assistant', 'content': 'The capital of Oman is Muscat.', 'refusal': None, 'annotations': []}, 
     'logprobs': None, 'finish_reason': 'stop'}
    ]
  , 'usage': {'prompt_tokens': 14, 'completion_tokens': 8, 'total_tokens': 22, 'prompt_tokens_details': {'cached_tokens': 0, 'audio_tokens': 0}, 'completion_tokens_details': {'reasoning_tokens': 0, 'audio_tokens': 0, 'accepted_prediction_tokens': 0, 'rejected_prediction_tokens': 0}}, 'service_tier': 'default', 'system_fingerprint': 'fp_41f1fe1393'}
  """


if __name__ == "__main__":
    main()
