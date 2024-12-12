import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from apikey import google_gemini_api_key


genai.configure(api_key=google_gemini_api_key)

# Function to get response from GEMINI PRO
def get_model_response(file, query):
    
    # Split the context into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    context = "\n\n".join(str(p.page_content) for p in file)

    data = text_splitter.split_text(context)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    searcher = Chroma.from_texts(data, embeddings).as_retriever()

    q = "Which employee has maximum salary?"
    records = searcher.get_relevant_documents(q)
    print(records)

    prompt_template = """
        You have to answer the question from the provided context and make sure that you provide all the details\n
        Context: {context}?\n
        Question: {question}\n
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.9)

    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    response = chain(
        {
            "input_documents": records,
            "question": query
        }
        , return_only_outputs=True
    )
    return response['output_text']
