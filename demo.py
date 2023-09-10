from langchain.document_loaders import UnstructuredFileLoader
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyMuPDFLoader
import os 


os.environ['OPENAI_API_KEY'] = "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"

def result(texts):

    loader = UnstructuredFileLoader("output.txt")
    document = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 0
    )
    texts = text_splitter.split_documents(document)
    persist_directory = "./storage"
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(documents=texts, 
                                    embedding=embeddings,
                                   )
    vectordb.persist()


    retriever = vectordb.as_retriever()
    llm = ChatOpenAI(model_name='gpt-4')
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    prompt_template = """You are a paralegal master in Taiwan's law.  \
        You should summary the content into three parts:
        請給我
        １．案由：結合案件背景，摘要出原告主張的內容與原因。
        """
    main_text="""２．主文：直接照抄判決主文。如果主文超過30字就請它幫忙摘要。"""
    summary="""３．理由要旨：法官的見解很重要，要適當引用法官的敘述。根據爭點分點寫出理由。所有的答案請用台灣風格的繁體中文回答
        在[理由要旨]中,著重法官的法理,再幫我就上述判決整理出符合我需要的格式的判決摘要。
        請總結以下判決結果，摘要中請著重法理論述:"""


    query = f"###Prompt 請總結以下判決結果，摘要中請著重法理論述:"
    list=[]
    try:
        cause = qa(prompt_template)
        print(cause["result"])
        maintext = qa(main_text)
        print(maintext["result"])
        Summary = qa(summary)
        print(Summary["result"])
    except Exception as err:
        print('Exception occurred. Please try again', str(err))
    return {'cause': cause["result"],'main_text':maintext["result"],"summary":Summary["result"]}