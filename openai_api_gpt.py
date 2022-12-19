import os
import openai



class ai_chat():

  def __init__(self, prompt):

    self.prompt = prompt


  def generate_response():

    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=self.prompt,
    temperature=0.7,
    max_tokens=709,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)

    return response.choices[0].text

  