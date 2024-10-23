import openai
from langchain_community.llms import HuggingFacePipeline
from langchain_huggingface import HuggingFaceEndpoint

"""
# Usage in another file

from llm import HuggingFaceModel, OpenAIMode

# Initialize Hugging Face Model
hf_model = HuggingFaceModel(repo_id="distilgpt2", huggingfacehub_api_token="your_token")
hf_response = hf_model.generate_text("Hello from Hugging Face!")

# Initialize OpenAI Model
openai_model = OpenAIModel(api_key="your_openai_api_key")
openai_response = openai_model.generate_text("Hello from OpenAI!")
"""


# Hugging Face Model Class
class HuggingFaceModel:
    def __init__(self, repo_id, huggingfacehub_api_token, temperature=1.0):
        self.repo_id = repo_id
        self.huggingfacehub_api_token = huggingfacehub_api_token
        self.temperature = temperature
        self.model = HuggingFaceEndpoint(
            repo_id=self.repo_id, 
            huggingfacehub_api_token=self.huggingfacehub_api_token,
            temperature=self.temperature  # If temperature is a valid parameter
        )
    def generate_text(self, prompt):
        # Call the model with the correct parameters
        response = self.model.invoke(prompt, parameters={"temperature": self.temperature})
        return response


# OpenAI Model Class
class OpenAIModel:
    def __init__(self, api_key, model_name="gpt-3.5-turbo", temperature=0.7):
        self.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        openai.api_key = api_key

    def generate_text(self, prompt):
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature
        )
        return response['choices'][0]['message']['content']

    ## Initialize the model with explicit parameters
    #model = HuggingFaceEndpoint(
    #    repo_id="distilgpt2",
    #    huggingfacehub_api_token=huggingface_token,
    #    temperature=1
    #)
    ## Pass the prompt as a list
    #response_text = model.generate([prompt])
