import boto3
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import random
import glob
import os 


def pull_file_from_s3(bucket, key):
    # Create a s3 client
    s3 = boto3.client('s3')
    s3.download_file(bucket, key, '/tmp/' + key.split("/")[-1])


def lambda_handler(event, context):
    pdf_docs = []
        # Pull the bucket and key from the event
    bucket = event["extension_finder"]["bucket_name"]
    key = event["extension_finder"]["object_key"]
    # Create a list of html_docs that will hold chunks
    # Pull or files from s3
    pull_file_from_s3(bucket, key)
    pdf_files = glob.glob(os.path.join("/tmp/", "*.pdf"))
    for _file in pdf_files:
        with open(_file) as f:
            # Create a BSHTMLLoader
            loader = PyPDFLoader(_file)
            # Load the html
            data = loader.load_and_split()
            # Create the splitter
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            # Split the data into chunks
            for page in data:
                chunks = text_splitter.split_documents(page)
                # Add the chunks the the list of html_docs
                pdf_docs.extend(chunks)

    return {
      "chunks": pdf_docs
    }

