import os 
import boto3
from langchain_community.document_loader import BSHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter



# Create a method to pull a file from s3 
def pull_file_from_s3(bucket, key):
    # Create a s3 client
    s3 = boto3.client('s3')

    # Pull the file from s3
    response = s3.get_object(Bucket=bucket, Key=key)

    # Return the file
    return response['Body'].read().decode('utf-8')


def lambda_handler(event, context):
    # Pull the bucket and key from the event
    bucket = event["extension_finder"]["bucket_name"]
    key = event["extension_finder"]["object_key"]
    # Create a list of html_docs that will hold chunks
    html_docs = []
    # Pull or files from s3
    html = pull_file_from_s3(bucket, key)
    # Create a BSHTMLLoader
    loader = BSHTMLLoader(html)
    # Load the html
    data = loader.load_html(html)
    # Create the splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # Split the data into chunks
    chunks = text_splitter.split_documents(data)
    # Add the chunks the the list of html_docs
    html_docs.extend(chunks)

    return {
      "chunks": html_docs
    }
