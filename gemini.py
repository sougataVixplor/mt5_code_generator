from google import genai
from google.genai import types
import pathlib
import httpx
import json
import os

def signal_data_extractor_prompt(signal_url):
    prompt=f"""
        Yor are the expert on MT5 signal source data scrapping. Analyze the images/videos/screenshots from the signal url -[{signal_url}]. After analyze the contents, generate similar/copy of MT5 code which
        can be executed in MT5Editor tool. Return on MT5 Code. Other informations are not required.
        """
    return prompt


def get_gemini_response(prompt,isJson=True):
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
  
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
        )
    data=response.text
    return data
