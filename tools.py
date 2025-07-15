import logging
import os
from langchain_google_vertexai import VertexAI, VertexAIEmbeddings
from google.oauth2 import service_account
from langchain_community.vectorstores import Typesense
import typesense

ts_config = {
    "api_key": "",
    "connectionTimeoutSeconds": "10",
    "nodes": [{ 		
        "host": "typesense-350195377988.us-central1.run.app",
        "port": "443", 
        "protocol": "https" 
    }]            
}

class Tools:
    def __init__(self):
        self.system_prompts = {}   
        self.llm = VertexAI(model_name="gemini-2.0-flash-lite")
        self.ts = typesense.Client(ts_config)

            
    def detect_intents(self, user_input: str):
        try:
            file_path = os.path.join(os.path.dirname(__file__), "./prompts/detect_intents.md")
            with open(file_path, "r", encoding="utf-8") as file:
                system_prompt = file.read()
        except:
            logging.warning("Prompt `detect_intents` not found locally.")
            return None

        prompt = system_prompt.format(user_input=user_input)
        response = self.llm.invoke(prompt)
        
        response.split("|||") if "|||" in response else [response]
        
        return response.split("|||") if "|||" in response else [response]


    def search_tool(self, intents: list[str]):
        try:
            embeddings=VertexAIEmbeddings(
                model_name="text-embedding-005",
            )   
            
            docsearch = Typesense(
                typesense_client=self.ts,
                embedding=embeddings,
                typesense_collection_name="tiebreak_demo",
            )

            retriever = docsearch.as_retriever()

            result = []
            for intent in intents:
                result.append(retriever.invoke(intent)[0].page_content)

            return result
            
        except Exception as e:
            logging.error(e, exc_info=True)
            return None    
        