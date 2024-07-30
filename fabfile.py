
import os     # Use to interface with the terminal 
import dotenv # Use to load environment variables

from source.utils import get_env_info_from_user, create_vectorstore # setup

#------------------------------------------------------------------
# Application Tasks - Using Fabfile module to make easy to call
# functions from the command line/terminal and keep the code clean 
#------------------------------------------------------------------

# Global Variables
vectorstore_folder = "./vectorstore"

#------------------------------------------------------------------
# Setup Task: 
# 1. Create .env file if not exists 
# 2. Load webpage info using BeautifulSoup and langchain 
# 3. Create embbeddings using langchain, chroma and save into vectorstore
from fabric import task
@task
def setup(c):
    api_key, rag_url = None, None
    
    # Check if .env file exists and create it if not
    if not dotenv.load_dotenv():
        print("[\x1b[31m Erro \x1b[0m] Arquivo de ambiente (.env) não encontrado.") 
        api_key, rag_url = get_env_info_from_user()

        if not api_key or not rag_url:
            return
        
        print("Criando um arquivo .env ...")
        with open(".env", "w") as f:
            f.write("GROQ_API_KEY=" + api_key)
            f.write("\nRAG_URL=" + rag_url)
        print("Arquivo .env criado com sucesso!\n")
    else:
        api_key = os.getenv("GROQ_API_KEY")
        rag_url = os.getenv("RAG_URL")
 
    # Create vectorstore from .env file info using langchain and chroma
    chunk_size         = 1000 
    chunk_overlap      = 200

    print("Iniciando uma Vectorstore apartir do link: " + rag_url) 
    print("Chunk_size = " + str(chunk_size))
    print("Chunk_overlap = " + str(chunk_overlap))
    print("Creating Vectorstore...")
    
    create_vectorstore(url=rag_url, chunk_size=1000, chunk_overlap=200, vectorstore_folder=vectorstore_folder)
    print("Feito! Vectorstore criada em " + vectorstore_folder) 

#------------------------------------------------------------------
# Run Task 
@task
def run(c):
    print("run web :)")
    pass

@task
def runCLI(c):
    user_input = input("Me pergunte algo: ")
