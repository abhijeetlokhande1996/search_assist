from langchain_core.messages import AIMessage, HumanMessage
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.chat_models import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from pathlib import Path

print("Loading OpenAI Embeddings")
embeddings = OpenAIEmbeddings()
index_path = Path(__file__).parent.parent / "products_openai_index"

new_db = FAISS.load_local(index_path, embeddings)
num_documents = len(new_db.index_to_docstore_id)

retriever = new_db.as_retriever()


# template = """You are an assistant for question-answering tasks.
# Use the following pieces of retrieved context to answer the question.
# If you don't know the answer, just say that you don't know.
# Use three sentences maximum and keep the answer concise.
# Question: {question}
# Context: {context}
# Answer:
# """
# prompt = ChatPromptTemplate.from_template(template)

# print(prompt)


llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# rag_chain = (
#     {"context": retriever,  "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )

# while True:
#     query = input("Enter query: ")
#     if query == "exit":
#         break
#     response = rag_chain.invoke(query)
#     print(response)


contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)
contextualize_q_chain = contextualize_q_prompt | llm | StrOutputParser()


contextualize_q_chain.invoke(
    {
        "chat_history": [
            HumanMessage(content="What does LLM stand for?"),
            AIMessage(content="Large language model"),
        ],
        "question": "What is meant by large",
    }
)
