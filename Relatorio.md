# Relatório de Implementação e Teste do Projeto LLMUcamp Chatbot  
  
Este relatório descreve o processo de desenvolvimento do projeto LLMUcamp Chatbot, incluindo o aprendizado sobre RAG (Retrieval-Augmented Generation), o uso e a exploração de bibliotecas como LangChain, BeautifulSoup e Streamlit, e a integração delas com um modelo Llama por meio do Groq. Combinando essas tecnologias open source, foi criado um assistente conversacional para informar sobre o vestibular da Unicamp 2025, com base na Resolução GR-029/2024, de 10/07/2024 (https://www.pg.unicamp.br/norma/31879/0). Ao final do processo, foi criado um conjunto de testes para avaliar o chatbot.

As principais ferramentas utilizadas no projeto foram:

- LLM: Llama3-70B-8192
- Framework para NLP: LangChain
- VectorStore: ChromaDB
- Interface Web: Streamlit
  
## Pesquisa e Análise Exploratória

Primeiramente, busquei me familiarizar com o conceito de Retrieval-Augmented Generation (RAG) e sua aplicação em tarefas de processamento de linguagem natural (NLP), para isso foi usado uma série de fontes onlines e após ter uma ideia inicial fiz uma várias perguntas ao ChaGPT e busquei checar as respostas por mim mesmo, assim pude validar de forma ativa e entender melhor sobre o assunto. Por fim tentei solidificar ao escrever rascunhos desse relatório explicando o RAG: 

### RAG (Retrieval-Augmented Generation)

RAG é uma técnica de NLP que combina recuperação de informações (retrieval) com geração de texto (generation). Esse método tem ganhado destaque por melhorar a qualidade e a precisão das respostas geradas por modelos de linguagem, especialmente aqueles baseados em redes neurais profundas. O que de fato condiz com a aplicação dessa técnica em ChatBots baseados em modelos Transformers como é caso desse projeto.

#### Recuperação de Informações (Retrieval)

Na primeira etapa, o modelo de RAG utiliza um componente de recuperação de informações para buscar dados relevantes em uma base de conhecimento pré-existente. Essa base de conhecimento pode ser composta por documentos, artigos, textos ou qualquer outro tipo de informação textual. O objetivo é encontrar fragmentos de texto que contenham informações relevantes para a pergunta ou contexto fornecido pelo usuário. Para realizar essa recuperação, RAG geralmente emprega modelos de embeddings, como o BERT ou outros modelos de Transformer, que são capazes de representar textos em um espaço vetorial. Quando uma consulta é feita, o modelo transforma tanto a consulta quanto os documentos em vetores e calcula a similaridade entre esses vetores para encontrar os textos mais relevantes.

#### Geração de Texto (Generation)

Uma vez recuperadas as informações relevantes, a segunda etapa envolve a geração de texto. Aqui, o modelo de RAG utiliza um componente de geração, como o GPT (Generative Pre-trained Transformer), para produzir uma resposta coerente e informativa. O diferencial é que, ao invés de gerar a resposta unicamente com base nos dados aprendidos durante o treinamento (como ocorre em modelos tradicionais de geração de texto), o RAG integra as informações recuperadas na primeira etapa, proporcionando respostas mais precisas e contextualizadas.

#### Integração das Etapas

A integração dessas duas etapas é o que torna o RAG tão poderoso. Quando uma consulta é recebida, o modelo de recuperação identifica as partes mais relevantes da base de conhecimento. Essas partes são então utilizadas como contexto adicional pelo modelo de geração, que combina esse contexto com seus próprios conhecimentos para produzir uma resposta final. Isso permite que o modelo acesse uma vasta quantidade de informações durante a geração de respostas, superando limitações comuns de modelos que dependem apenas do conhecimento aprendido durante o treinamento.

### Leitura da Resolução 

A seguir, foi realizada a leitura da Resolução GR-029/2024 para se familiarizar com o conteúdo e facilitar a elaboração de perguntas baseadas nessa base de dados. O documento é bem extenso, em formato de PDF teria por volta de 99 páginas segundo a ferramente de impressão, ele, no geral, é  estruturado em artigos e anexos. Durante essa leitura utilizei do ChatGPT para resumir alguns dos paragrafos para meu melhor entendimento. Embora a maior parte do conteúdo seja em texto, algumas informações estão apresentadas em formato de tabela. Com isso em mente, optei por utilizar ferramentas da LangChain, juntamente com pacotes de web scraping, para extrair as informações necessárias para o nosso ChatBot. Essa etapa foi crucial para garantir uma compreensão detalhada do material e permitir a criação de perguntas relevantes e bem fundamentadas.

#### Fontes usadas:
- https://aws.amazon.com/pt/what-is/retrieval-augmented-generation/
- https://cloud.google.com/use-cases/retrieval-augmented-generation
- https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/
- https://triggo.ai/blog/o-que-e-retrieval-augmented-generation/
- https://research.ibm.com/blog/retrieval-augmented-generation-RAG
- https://www.pg.unicamp.br/norma/31879/0 


## Implementação e Metodologia

Como apresentado na documentação o código desse projeto inteiro está contido em apenas 4 arquivos: `fabfile.py`, `source/utils.py`, `source/LLMUcamp.py`, `streamlit_app.py`. Primeiro será descrito o funcionamento do projeto de forma geral e em seguida será detalhado o que cada módulo faz

### Funcionamento

O sistema é estruturado em vários módulos que colaboram para criar uma aplicação de chatbot eficiente, utilizando a arquitetura RAG. O **módulo de gerenciamento de tarefas** coordena a configuração e execução do sistema, facilitando a preparação do ambiente, execução de testes e lançamento da aplicação. Ele garante que as variáveis de ambiente estejam corretamente configuradas e que a vectorstore seja criada e gerenciada.

O **módulo utilitário** fornece funções auxiliares para carregar e processar dados. Ele é responsável por criar e carregar a vectorstore a partir de documentos e textos, que são essenciais para o sistema de recuperação de informações. Este módulo integra ferramentas de carregamento de documentos, divisão de texto e criação de embeddings, preparando os dados para consulta e recuperação.

A **classe de chatbot** configura o modelo de linguagem e o sistema de recuperação. Utiliza a vectorstore criada pelo módulo de utilitários para recuperar informações relevantes e gerar respostas baseadas no contexto da pergunta. Ela configura um modelo de linguagem com um prompt específico e implementa um mecanismo de recuperação que combina dados do contexto com o modelo de linguagem.

Finalmente, o **módulo de interface de usuário** oferece uma camada interativa para os usuários. Utilizando uma aplicação web, ele permite que os usuários façam perguntas e recebam respostas do chatbot. Este módulo se comunica com a classe de chatbot para obter e exibir as respostas em uma interface amigável. No contexto de um sistema RAG, a integração desses módulos permite a recuperação e geração de respostas precisas, combinando dados armazenados com um modelo de linguagem treinado para oferecer uma experiência de interação enriquecida e contextualizada.

### Fabfile

O arquivo `fabfile.py` utiliza a biblioteca **Fabric** para automação de tarefas, facilitando a execução de funções a partir da linha de comando e tornando o projeto mais facilmente escalável. Ele é responsável por gerenciar a configuração e execução do projeto. Entre suas principais funções, o `setup` cria um arquivo **.env** se não existir, solicitando informações ao usuário para configurar a variável de ambiente necessária. O código para criar o arquivo .env é o seguinte:

```python
if not dotenv.load_dotenv():
    api_key, rag_url = get_env_info_from_user()
    with open(".env", "w") as f:
        f.write("GROQ_API_KEY=" + api_key + "\nRAG_URL=" + rag_url)
```
Além disso, o `fabfile.py` inclui tarefas para executar o chatbot na linha de comando (`runCLI`) e iniciar a aplicação web Streamlit (`runWeb`). A tarefa `test` realiza testes automatizados, perguntando ao chatbot e salvando as respostas, permitindo a verificação da funcionalidade do modelo de linguagem. Importante comentar também que é nesse arquivo que define o LLM base para o chatbot (todos por meio do módulo Groq), experimentei com os 3 abaixo:

- llama3-70b-8192
- llama-3.1-70b-versatile
- mixtral-8x7b-3276

### Utils

O arquivo `source/utils.py` define várias funções auxiliares que suportam a configuração e operação do projeto. Utilizando bibliotecas como `BeautifulSoup (bs4)` para webscrapping e análise de HTML e `LangChain` para processamento de linguagem, este arquivo é crucial para a criação e manipulação da vectorstore. A função `create_vectorstore`, por exemplo, carrega documentos de um URL e cria embeddings para armazenar em uma vectorstore construída com o módulo `Chroma`, que é uma opção lightweight, user-friendly e open-source de um sistema de armazenamento de embeddings vetoriais para modelos de linguagem, e por isso a escolhi invês do usual `FAISS`

```python
def create_vectorstore(docs_url, chunk_size, chunk_overlap, vectorstore_folder):  
	...  
	# Load webpage using langchain and bs4  
	soup_strainer = bs4.SoupStrainer(class_=("card-body"))  
	web_loader = WebBaseLoader(web_paths=(docs_url,), bs_kwargs={"parse_only": soup_strainer})  
	docs = web_loader.load()  
	  
	# Split text into smaller chunks  
	text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True)  
	docs = text_splitter.split_documents(docs)  
	  
	# Create embeddings using langchain and chroma  
	vectorstore = Chroma.from_documents(documents=docs, embedding=HuggingFaceEmbeddings(), persist_directory=vectorstore_folder)  
```
Como pode ser observado os embeddings foram criados com o auxilio do módulo `HuggingFaceEmbeddings`. Além disso, o arquivo contém funções para carregar a vectorstore e obter caminhos para arquivos de texto, essenciais para o funcionamento e testes do chatbot.

### LLMUcamp

O source/LLMUcamp.py define a classe LLMUcamp, que encapsula a lógica do chatbot. Utilizando a biblioteca `langchain_groq`, a classe configura um modelo de linguagem e um sistema de recuperação de informações. A parte do código  que inicializa o chatbot e configurar o prompt de seu comportamento é o seguinte:

```python
class LLMUcamp():  
def __init__(self, vectorstore_folder, model, temperature):  
	self.vectorstore_retriever = utils.load_vectorstore(vectorstore_folder)  
	  
	base_llm = ChatGroq(temperature=temperature, model=model)  
	system_prompt = (  
	"Você é um assistente virtual responsável por responder dúvidas sobre o Vestibular da Unicamp 2025."  
	"Como fonte de informação, você usará a Resolução GR-029/2024, de 10/07/2024."  
	"Você deverá considerar o histórico da conversa, o contexto e a pergunta dada para fornecer uma resposta."  
	"Caso não saiba uma resposta não tente inventar alguma, responda que não tem uma resposta" 
	"\n\n"  
	"{context}"  
	)  
	  
	prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])  
	answer_chain = create_stuff_documents_chain(base_llm, prompt)  
	self.rag_chain = create_retrieval_chain(self.vectorstore_retriever, answer_chain)  
  
def answer(self, question):  
	response = self.rag_chain.invoke({"input": question})  
	return response.get("answer")
```
A classe fornece uma interface para responder perguntas utilizando o modelo e a vectorstore configurados, permitindo a geração de respostas baseadas em um contexto específico e informações armazenadas. Isso permite que a interação com o chatbot seja mais modular em questão de código, assim o modo CLI e WEB foram mais fáceis de serem feitos

Durante a implementação, testei várias chains da biblioteca `LangChain`, como a `ConversationalRetrievalChain` mas acabou que a abordagem mais satisfatória e flexível foi a que envolveu a construção explícita dos prompts e o retrieval de documentos.

### Streamlit-app

O arquivo streamlit_app.py implementa a interface de usuário do chatbot utilizando a biblioteca `Streamlit`. A aplicação web exibe um chat onde os usuários podem interagir com o chatbot. A função launch_app configura a interface e gerencia a exibição das mensagens:

```python
def launch_app(chatbot: LLMUcamp, user_icon, chatbot_icon):  
	st.title("🎓 Chatbot Vestibular Unicamp 2025 - LLMUcamp")  	  
	avatar_dict = {"user": user_icon, "assistant": chatbot_icon}  
	  
	# Initialize the chat messages history  
	if "messages" not in st.session_state.keys():  
	st.session_state.messages = [{  
		"role": "assistant",  
		"content": "Olá! Estou aqui para ajudar..."
	}]  
	  
	# Prompt for user input and save  
	if prompt := st.chat_input():  
	st.session_state.messages.append({"role": "user", "content": prompt})  
	  
	# Display the existing chat messages  
	for message_data in st.session_state.messages:  
	role = message_data["role"]  
	content = message_data["content"]  
	with st.chat_message(role, avatar=avatar_dict[role]):  
	st.markdown(f"{content}")  
	  
	# If last message is not from assistant, 
	# we need to generate a new answer  
	if st.session_state.messages[-1]["role"] != "assistant":  
	# Call the chatbot function  
	with st.chat_message("assistant", avatar=avatar_dict["assistant"]):  
	with st.spinner("Pensando..."):  
	answer = chatbot.answer(prompt)
	st.write_stream(typed_answer(answer))  
	  
	message = {"role": "assistant", "content": answer}  
	st.session_state.messages.append(message)
```
A interface é personalizada de forma que:
- O avatares da conversa fossem mais relacionados com o objetivo.
- As mensagens do bot e do usuário fiquem em lados opostos para que fique mais similar a um chat de rede social
- A resposta do chatbot é gerada e exibida com um efeito de digitação para simular uma conversa natural.

#### Fontes usadas:
- https://python.langchain.com/v0.2/docs/tutorials/chatbot/
- https://console.groq.com/docs/quickstart
- https://python.langchain.com/v0.2/docs/integrations/text_embedding/sentence_transformers/
- https://docs.streamlit.io/get-started/tutorials/create-an-app
- https://dev.to/peterabel/what-chunk-size-and-chunk-overlap-should-you-use-4338
- https://docs.streamlit.io/


## Testes e Avaliação

### Testes 

Para avaliar o chatbot foi desenvolvido 2 conjuntos de teste. O primeiro contendo 100 perguntas geradas pelo ChatGPT acerca do vestibular da Unicamp. E o segundo contendo 10 perguntas criadas por um ser humano. Ambos os conjuntos estão em arquivos .txt na pasta `tests_data/questions`. Ao rodar o comando abaixo cada uma das perguntas será passada ao chatbot e as respostas serão salvas na pasta `tests_data/answers`

```bash
fab test
```

Caso deseje adicionar suas próprias perguntas basta criar um arquivo .txt com elas dentro da pasta `tests_data/questions` (precisam estar numeradas)

### Avaliação

Avaliando manualmente as respostas dos testes nos arquivos .txt foi possivel concluir não só que o melhor modelo base foi o `llama-3.1-70b-versatile` como todos eles conseguiram  capturar um bom conhecimento relacionado ao Vestibular da Unicamp 2025. As perguntas em que ele se saiu melhor foram as mais abertas e que pedem instruções ou perguntam sobre a existência de algo, o que indica um bom comportamento como assistente simples. Porém, ficou notável algumas dificuldades em perguntas mais objetivas como as datas de inscrição do vestibular ou números de vagas, acredito que tenha haver com a questão de obter informações sobre as tabelas. Importante comentar que depois que o preview do Groq do modelo `llama-3.1-70b-versatile` atingiu o seu limite passei a utilizar o `llama-3-70b-8192` que não tinha esse limite, assim todas as ferramentas usadas no projeto foram gratuitas.

## Uso do ChatGPT

Ao longo do relatório foi explicado em maiores detalhes cada parte que utilizei o ChatGPT, mas para fins de organização aqui está uma lista de atividades em que ele foi útil:

- Clarificar e responder minhas dúvidas sobre RAG
- Resumo de paragrafos da resolução do vestibular da unicamp 2025
- Auxiliar de documentação do Streamlit e do LangChain
- Geração de 100 perguntas para teste do chatbot
- Correção e melhora de textos para a documentação e relatório
