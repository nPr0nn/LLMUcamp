
import os     # Use to interface with the terminal 
import dotenv # Use to load environment variables

from source.LLMUcamp import LLMUcamp
from source.utils import get_env_info_from_user, create_vectorstore # setup

from streamlit.web import cli 

#------------------------------------------------------------------
# Application Tasks - Using Fabfile module to make easy to call
# functions from the command line/terminal and keep the code clean 
#------------------------------------------------------------------

# Global Variables (only paths and icons)
vectorstore_folder = "./vectorstore"
user_icon          = "assets/nerd-face.svg"
chatbot_icon       = "assets/UNICAMP_logo.svg" 

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
    create_vectorstore(docs_url=rag_url, chunk_size=1000, chunk_overlap=200, vectorstore_folder=vectorstore_folder) 
    print("Feito! Vectorstore criada em " + vectorstore_folder) 

#------------------------------------------------------------------
# Run Task: 
@task
def runCLI(c):
    if not dotenv.load_dotenv():
        print("[\x1b[31m Erro \x1b[0m] Arquivo de ambiente (.env) não encontrado.") 
        return
    
    chatbot = LLMUcamp(vectorstore_folder=vectorstore_folder, temperature=0, model="llama-3.1-70b-versatile")
    while(user_question := input("Faça sua pergunta: ")):
        print(chatbot.answer(user_question))

@task
def runWeb(c):
    if not dotenv.load_dotenv():
        print("[\x1b[31m Erro \x1b[0m] Arquivo de ambiente (.env) não encontrado.") 
        return
    
    args = vectorstore_folder + " " + user_icon + " " + chatbot_icon 
    os.system("streamlit run streamlit_app.py " + args)
