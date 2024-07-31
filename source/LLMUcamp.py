

from . import utils

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

class LLMUcamp():  
    def __init__(self, vectorstore_folder, model, temperature):
        self.vectorstore_retriever = utils.load_vectorstore(vectorstore_folder)

        base_llm = ChatGroq(temperature=temperature, model=model) 
        system_prompt = (
            "Você é um assistente virtual responsável por responder dúvidas sobre o Vestibular da Unicamp 2025."
            "Como fonte de informação, você usará a Resolução GR-029/2024, de 10/07/2024."
            "Você deverá considerar o histórico da conversa, o contexto e a pergunta dada para fornecer uma resposta."
            "Caso não saiba uma resposta não tente inventar alguma, responda que não tem uma resposta"
            "Não responda dúvidas não relacionadas a pergunta feita."
            "Assuma que todas as dúvidas são acerca do Vestibular da Unicamp 2025. E sempre responda em portugues."
            "\n\n"
            "{context}"
        )

        prompt         = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
        answer_chain   = create_stuff_documents_chain(base_llm, prompt)
        self.rag_chain = create_retrieval_chain(self.vectorstore_retriever, answer_chain) 
    
    def answer(self, question):
        response = self.rag_chain.invoke({"input": question})
        return response.get("answer") 
