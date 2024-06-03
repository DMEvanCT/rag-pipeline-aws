import boto3
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import glob
import os 
from aws_lambda_powertools import Logger

logger = Logger()

def pull_file_from_s3(bucket, key):
    # Create a s3 client
    s3 = boto3.client('s3')
    s3.download_file(bucket, key, '/tmp/' + key.split("/")[-1])

@logger.inject_lambda_context
def lambda_handler(event, context):
    pdf_docs = []
    # Pull the bucket and key from the event
    bucket = event["extension_finder"]["bucket_name"]
    key = event["extension_finder"]["object_key"]
    
    # Pull the file from S3
    pull_file_from_s3(bucket, key)
    
    # Find all PDF files in the /tmp/ directory
    pdf_files = glob.glob(os.path.join("/tmp/", "*.pdf"))
    
    for _file in pdf_files:
        # Load the PDF file
        pdf_loader = PyPDFLoader(_file)
        data = pdf_loader.load_and_split()
        for page in data:
            logger.debug(page.metadata)
            logger.debug(page.page_content)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunk = text_splitter.split_text(page.page_content)
            pdf_docs.append({"text": chunk, "metadata": page.metadata})
        

    return {
        "chunks": pdf_docs
    }