import os
from dotenv import load_dotenv

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyMuPDFLoader


os.environ['OPENAI_API_KEY'] = "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"
loader = PyMuPDFLoader("./data/judgement.pdf")
documents = loader.load()
# print(documents)


# corpus = "The concept of TextSplitters revolves around the need to break down long pieces of text into smaller"

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=10)
texts = text_splitter.split_documents(documents)


persist_directory = "./storage"
embeddings = OpenAIEmbeddings()
vectordb = Chroma.from_documents(documents=texts, 
                                 embedding=embeddings,
                                 persist_directory=persist_directory)
vectordb.persist()


retriever = vectordb.as_retriever()
llm = ChatOpenAI(model_name='gpt-4')
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

prompt_template = "You are a paralegal master in Taiwan's law.  \
    You should summary the content into three parts:1. 爭點2.主文 3.理由要旨. 所有的答案請用台灣風格的繁體中文回答"

user_input = "請總結本判決"

query = f"###Prompt {user_input}"
try:
    llm_response = qa(query)
    print(llm_response["result"])
except Exception as err:
    print('Exception occurred. Please try again', str(err))