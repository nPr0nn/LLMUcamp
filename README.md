
# Documentação do Projeto LLMUcamp Chatbot

## Visão Geral

O Projeto LLMUcamp Chatbot é projetado para fornecer um chatbot interativo para responder perguntas sobre o Vestibular da UNICAMP 2025. O projeto utiliza várias bibliotecas e ferramentas, incluindo Streamlit para a interface web, LangChain para processamento de linguagem natural e Chroma para gerenciamento de vectorstores.

## Demo 

Fale com o LLMUcamp Chatbot online em: **colocar link

## Estrutura do Projeto

1. **`fabfile.py`** - Contém tasks para configurar o ambiente e executar o chatbot tanto em modo CLI ou em modo web com Streamlit.
2. **`source/utils.py`** - Fornece algumas funções auxiliares para o chatbot como o gerenciamento de VectorStores do LangChain.
3. **`source/LLMUcamp.py`** - Define a classe `LLMUcamp` para lidar com interações do chatbot e recuperação de embeddings.
4. **`streamlit_app.py`** - Implementa a interface web Streamlit para o chatbot.

## Instalação

### Pré-requisitos

Certifique-se de que você tem Python 3.8+ e `pip` instalados. Em seguida basta baixar o .zip desse repositório ou o clonar com o comando:

```bash
git clone https://github.com/nPr0nn/LLMUcamp.git
```

### Dependências

Dentro da pasta LLMUcamp. Instale os pacotes Python necessários usando:

```bash
pip install -r requirements.txt
```

### Configuração 

Execute a tarefa `setup` para inicializar configurar o ambiente:

```bash
fab setup
```

Esse comando irá:

- Criar um arquivo `.env` com as variáveis de ambiente `GROQ_API_KEY` e `RAG_URL` caso o arquivo `.env` não exista. A chave de acesso para o API do Groq (`GROQ_API_KEY`) será requisitada ao usuário na primeira execução desse comando e ela será guardada apenas **localmente** no arquivo `.env`.
- Inicializar a VectorStore com os embeddings referentes à página determinada na url `RAG_URL`. Por padrão essa página é <https://www.pg.unicamp.br/norma/31879/0> que contém a  publicação da Resolução GR-029/2024, de 10/07/2024 que "Dispõe sobre o Vestibular Unicamp 2025 para vagas no ensino de Graduação".

[![Imagem](/assets/repo/setup.png)]

## Uso

### Executar o chatbot em modo CLI 

Para iniciar a interface de linha de comando do chatbot, use a tarefa runCLI:

```bash
fab runCLI
```

[![Imagem](/assets/repo/cli.png)]

### Executar o chatbot na web com Streamlit

Para iniciar a interface web do chatbot, use a tarefa runWeb:

```bash
fab runWeb
```

[![Imagem](/assets/repo/web1.png)]
[![Imagem](/assets/repo/web2.png)]


## Testes

