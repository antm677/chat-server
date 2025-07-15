import logging
from langchain_google_vertexai import VertexAIEmbeddings
import typesense
from langchain_community.vectorstores import Typesense
from langchain.schema.document import Document
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

schema = {
  "name": "tiebreak_demo",
  "fields": [
    {
      "name": "vec",
      "type": "float[]",
      "facet": False,
      "optional": False,
      "index": True,
      "sort": False,
      "infix": False,
      "locale": "",
      "hnsw_params": {
        "M": 16,
        "ef_construction": 200
      },
      "num_dim": 768,
      "stem": False,
      "store": True,
      "vec_dist": "cosine"
    },
    {
      "name": "text",
      "type": "string",
      "facet": False,
      "optional": False,
      "index": True,
      "sort": False,
      "infix": False,
      "locale": "",
      "stem": False,
      "store": True
    },
    {
      "name": ".*",
      "type": "auto",
      "facet": False,
      "optional": True,
      "index": True,
      "sort": False,
      "infix": False,
      "locale": "",
      "stem": False,
      "store": True
    }
  ],
  "default_sorting_field": "",
  "enable_nested_fields": False,
  "symbols_to_index": [],
  "token_separators": []
}


def create_vector_store(docs: list[Document]):
    try:
        embeddings=VertexAIEmbeddings(
            model_name="text-embedding-005",
        )

        ts = typesense.Client(ts_config)
        try:
            ts.collections[schema["name"]].delete()
        except typesense.exceptions.ObjectNotFound as e:
            logging.info(f"Failed to delete collection tiebreak_demo because it doesn't exists.")
            pass

        try:
            ts.collections.create(schema)
        except typesense.exceptions.ObjectAlreadyExists as e:
            logging.info(f"Collection {schema["name"]} already exists.")
            pass

        Typesense.from_documents(
            docs,
            embeddings,
            typesense_client_params={
                "host": ts_config["nodes"][0]["host"],
                "port": ts_config["nodes"][0]["port"],
                "protocol": ts_config["nodes"][0]["protocol"],
                "typesense_api_key": ts_config["api_key"],
                "typesense_collection_name": "tiebreak_demo",
            },
        )

        return True
        
    except Exception as e:
        logging.error(e, exc_info=True)
        return False


def retrieve_from_vectore_store(query: str):
    try:
        typesense_client = typesense.Client(ts_config)
        
        embeddings=VertexAIEmbeddings(
            model_name="text-embedding-005"
        )   
        
        docsearch = Typesense(
            typesense_client=typesense_client,
            embedding=embeddings,
            typesense_collection_name="tiebreak_demo",
        )

        retriever = docsearch.as_retriever()

        return retriever.invoke(query)[0].page_content
        
    except Exception as e:
        logging.error(e, exc_info=True)
        return None