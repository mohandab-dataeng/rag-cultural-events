"""
Chatbot RAG : orchestre la recherche FAISS et la génération Mistral via LCEL (API stable, post LangChain 1.0).
"""
import os
import time
from dotenv import load_dotenv
from langchain_mistralai import MistralAIEmbeddings, ChatMistralAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

SYSTEM_PROMPT = """Tu es un assistant qui aide les utilisateurs à trouver des événements culturels en Île-de-France.
Réponds à la question en te basant UNIQUEMENT sur les événements fournis dans le contexte ci-dessous.
Si l'information n'est pas dans le contexte, dis que tu ne trouves pas d'événement correspondant.

Contexte (événements pertinents) :
{context}"""


def load_vector_store(path="index_faiss"):
    embeddings = MistralAIEmbeddings(
        model="mistral-embed",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
    )
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)

def format_docs(docs):
    """Colle le texte de tous les documents trouvés en une seule string : c'est ÇA, concrètement, le 'stuff'."""
    return "\n\n".join(doc.page_content for doc in docs)

def build_rag_chain(vector_store):
    llm = ChatMistralAI(
    model="mistral-small-latest",
    mistral_api_key=os.getenv("MISTRAL_API_KEY"),
    temperature=0.2,
    max_retries=1,  # évite les rafales de retry qui aggravent le 429
)

    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])

    generation_chain = prompt | llm | StrOutputParser()
    return retriever, generation_chain

def ask_question(retriever, generation_chain, question):
    sources = retriever.invoke(question)
    context = format_docs(sources)
    time.sleep(1.5)  # respecte la limite de 1 req/seconde
    reponse = generation_chain.invoke({"context": context, "question": question})
    return reponse, sources

if __name__ == "__main__":
    print("Chargement de l'index FAISS...")
    vector_store = load_vector_store()

    print("Construction de la chaîne RAG...")
    retriever, generation_chain = build_rag_chain(vector_store)

    print("Chatbot prêt. Tape 'exit' pour quitter.\n")
    while True:
        question = input("Question : ")
        if question.lower() == "exit":
            break

        reponse, sources = ask_question(retriever, generation_chain, question)
        print(f"\nRéponse : {reponse}\n")
        print("Sources :")
        for doc in sources:
            print(f"  - {doc.metadata['title']} ({doc.metadata['city']})")
        print()