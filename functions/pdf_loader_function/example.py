from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import glob
import os 



def main():
    pdf_docs = []
    pdf_files = glob.glob(os.path.join("./pdf", "*.pdf"))

    for _file in pdf_files:
        # Load the PDF file
        pdf_loader = PyPDFLoader(_file)
        data = pdf_loader.load_and_split()
        print(len(data))
        for page in data:
            print(page.metadata)
            print(page.page_content)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunk = text_splitter.split_text(page.page_content)
            #print("Chunk: ")
            #print(chunk)
            content_dict = {"text": chunk, "metadata": page.metadata}
            pdf_docs.append(content_dict)

    print("PDF Docs: ")
    print(pdf_docs)


    return {
        "chunks": pdf_docs
    }
    
if __name__ == "__main__":
    main()