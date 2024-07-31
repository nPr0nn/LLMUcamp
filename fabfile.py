
import os     # Use to interface with the terminal 
import dotenv # Use to load environment variables

from source.LLMUcamp import LLMUcamp
from source.utils import get_env_info_from_user, create_vectorstore # setup

from streamlit.web import cli 

from source.utils import get_txt_file_paths

#------------------------------------------------------------------
# Application Tasks - Using Fabfile module to make easy to call
# functions from the command line/terminal and keep the code clean 
#------------------------------------------------------------------

# Global Variables (only paths and icons)
default_model              = "llama3-70b-8192"
# default_model              = "llama-3.1-70b-versatile"
# default_model              = "mixtral-8x7b-32768"

vectorstore_folder = "./vectorstore"
user_icon          = "assets/chatbot/nerd-face.svg"
chatbot_icon       = "assets/chatbot/UNICAMP_logo.svg" 

tests_folder       = "./tests_data"

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
# 1. Run CLI
# 2. Run Web
@task
def runCLI(c):
    if not dotenv.load_dotenv():
        print("[\x1b[31m Erro \x1b[0m] Arquivo de ambiente (.env) não encontrado.") 
        return
    
    chatbot = LLMUcamp(vectorstore_folder=vectorstore_folder, temperature=0, model=default_model)
    while(user_question := input("Faça sua pergunta: ")):
        print(chatbot.answer(user_question))

@task
def runWeb(c):
    if not dotenv.load_dotenv():
        print("[\x1b[31m Erro \x1b[0m] Arquivo de ambiente (.env) não encontrado.") 
        return
    
    args = vectorstore_folder + " " + user_icon + " " + chatbot_icon + " " + default_model 
    os.system("streamlit run streamlit_app.py " + args)

#------------------------------------------------------------------
# Test Task:
@task
def test(c):
    if not dotenv.load_dotenv():
        print("[\x1b[31m Erro \x1b[0m] Arquivo de ambiente (.env) não encontrado.") 
        return

    # Get chatbot
    chatbot = LLMUcamp(vectorstore_folder=vectorstore_folder, temperature=0, model=default_model)
    
    # Get questions data
    questions_folder_path = os.path.join(tests_folder, "questions") 
    answers_folder_path = os.path.join(tests_folder, "answers")
    questions_files = get_txt_file_paths(questions_folder_path) 

    # Test
    for question_file in questions_files:
        answers_file = question_file.replace(questions_folder_path, answers_folder_path)  
        answers      = [] 
      
        with open(question_file, "r") as file:
            questions = file.readlines()

        with open(answers_file, "w") as file:
            file.writelines("Origin file: " + question_file + "\n\n")
            
            for question in questions:
                pure_question = question.split(".")[1].strip("\n")
                answer        = chatbot.answer(pure_question)
                bar = "----------------------------------------------------------------------------"
                answers.append(f"{bar}\n\n{question}\n[Resposta]\n{answer}\n\n")
                print(answers[-1]) 
                file.writelines(answers[-1]) 
    return
