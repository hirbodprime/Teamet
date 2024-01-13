
from rest_framework.views import APIView
from rest_framework.response import Response

from openai import OpenAI
from dotenv import load_dotenv

import os

load_dotenv()

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY"),
  organization=os.getenv("OPENAI_ORG_API_KEY")
)

class OpenAIChatInteractionView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_prompt = request.data.get('user_text_prompt')
        history = request.data.get('user_text_history')
        key = request.data.get('key')
        if key == "TheKey!1@":
            if user_prompt:
                if history:
                    chat_history_messages = [
                        {"role": "assistant", "content": history}
                    ]

                    messages = [
                        {"role": "system", "content": "You are a helpful assistant."},
                        *chat_history_messages,
                        {"role": "user", "content": user_prompt}
                    ]
                else:
                    messages = [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_prompt}
                    ]


                completion = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages
                )

                # Extract GPT response message
                gpt_response = completion.choices[0].message.content

                return Response({"gpt_response": gpt_response})
            return Response({"gpt_response": 'user_text_prompt is needed'})
            
        return Response({"gpt_response": 'Your Are not Allowed'})
