import boto3
import os
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def get_parameter_store_parameters(parameter_name: str):
    # Create a SSM client
    ssm = boto3.client('ssm')
    # Get the value of the parameter
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    return response["Parameter"]["Value"]


def lambda_handler(event, context):
    chunks_and_metadata = event['loader']['chunks']
    
    pinecone_api_key = get_parameter_store_parameters("/pinecone/api_key")
    pinecone_index_name = get_parameter_store_parameters("/pinecone/index_name")
    openai_api_key = get_parameter_store_parameters("/openai/api_key")

    os.environ["PINECONE_API_KEY"] = pinecone_api_key
    os.environ["OPENAI_API_KEY"] = openai_api_key

   # 3072 is the dimension of the text-embedding-3-large model 
    embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    deployment="text-embedding-3-large",
    max_retries=0

    texts = [chunk["text"] for chunk in chunks_and_metadata]
    metadata = [chunk["metadata"] for chunk in chunks_and_metadata]
    print(texts)

    PineconeVectorStore.from_texts(
        texts=texts,
        index_name=pinecone_index_name,
        embedding=embeddings,
        metadatas=metadata
    )
