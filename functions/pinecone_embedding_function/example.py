from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os
chunks_and_metadata = [
    {"text": "text1", "metadata": {"key1": "value1"}},
    {"text": "text2", "metadata": {"key2": "value2"}},
    {"text": "text3", "metadata": {"key3": "value3"}},
    {"text": "text4", "metadata": {"key4": "value4"}},
    {"text": "text5", "metadata": {"key5": "value5"}},
    {"text": "text6", "metadata": {"key6": "value6"}},
    {"text": "text7", "metadata": {"key7": "value7"}},
    {"text": "text8", "metadata": {"key8": "value8"}},
    {"text": "text9", "metadata": {"key9": "value9"}},
    {"text": "text10", "metadata": {"key10": "value10"}},
]

# 3072 is the dimension of the text-embedding-3-large model 
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    deployment="text-embedding-3-large",
    max_retries=0
)

texts = [chunk["text"] for chunk in chunks_and_metadata]
metadata = [chunk["metadata"] for chunk in chunks_and_metadata]
print(texts)

PineconeVectorStore.from_texts(
    texts=texts,
    index_name='quickstart',
    embedding=embeddings,
    metadatas=metadata
)