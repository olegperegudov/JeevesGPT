import argparse
import os

from dotenv import find_dotenv, load_dotenv

import openai

_ = load_dotenv(find_dotenv())  # read local .env file

parser = argparse.ArgumentParser()
parser.add_argument("fname", type=str)
fname, _ = parser.parse_known_args()


openai.api_key = os.getenv("OPENAI_API_KEY")


def get_completion(
    prompt, model="gpt-3.5-turbo"
):  # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


# PROMPT
subtitles_path = os.path.join(os.getcwd(), "data", "subtitles", f"{fname}.txt")
with open(subtitles_path, "r") as file:
    subtitles = file.read().replace("\n", "")

prompt = f"""
Your task is to generate a short summary of a youtube video subtitles.
Summarize the subtitles below, delimited by triple 
backticks.
Summary: ```{subtitles}```
"""

# RESPONSE
response = get_completion(prompt)
# save response to file in data/summaries
fpath = os.path.join(os.getcwd(), "data", "summaries", f"{fname}.txt")
with open(fpath, "w") as file:
    file.write(response)

print(response)
