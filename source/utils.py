
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

#------------------------------------------------------------------

def get_env_info_from_user():    
    # Get user input to create .env file
    print("\nParece que você ainda não tem um arquivo de ambiente (.env)...")
    create_env = input("Você quer criar um ? s/n: ").replace(" ", "") 
    while create_env not in ["s", "n"]:
        create_env = input("Por favor, insira 's' ou 'n': ").replace(" ", "")

    # Goodbye message
    if create_env == "n":
        print("Ok, até a próxima ;)")
        return None, None

    print("\nPara criar um arquivo de ambiente, você precisará fornecer algumas informações")
    print("Não se preocupe, isso é apenas local no seu computador e não será compartilhado com ninguém\n")

    # Environment File Variables
    api_key = input("Por favor, insira sua chave da API Groq: ").replace(" ", "")
    rag_url = "https://www.pg.unicamp.br/norma/31879/0" # constante para este projeto

    return api_key, rag_url

#------------------------------------------------------------------

def create_vectorstore(docs_url, chunk_size, chunk_overlap, vectorstore_folder):    
    print("Iniciando uma Vectorstore apartir do link: " + docs_url) 
    print("Chunk_size = " + str(chunk_size))
    print("Chunk_overlap = " + str(chunk_overlap))
    print("Creating Vectorstore...")
    
    # Load webpage using langchain and bs4
    soup_strainer = bs4.SoupStrainer(class_=("card-body"))
    web_loader    = WebBaseLoader(web_paths=(docs_url,), bs_kwargs={"parse_only": soup_strainer})
    docs          = web_loader.load()

    # Split text into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True)
    docs          = text_splitter.split_documents(docs)

    # Create embeddings using langchain and chroma
    vectorstore = Chroma.from_documents(documents=docs, embedding=HuggingFaceEmbeddings(), persist_directory=vectorstore_folder)
    return vectorstore 

def load_vectorstore(vectorstore_folder):
    vectorstore = Chroma(persist_directory=vectorstore_folder, embedding_function=HuggingFaceEmbeddings()) 
    return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

#------------------------------------------------------------------
