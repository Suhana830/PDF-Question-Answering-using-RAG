from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

from langchain_chroma import Chroma


load_dotenv()

# ---------- LLM ----------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# ---------- Splitter ----------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# ---------- Embeddings + Vector DB ----------
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = Chroma(
    embedding_function=embeddings,
    collection_name="mycollection",
    
    
)


def function_upload_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    split_text = splitter.split_documents(docs)
    

    vector_store.add_documents(split_text)
    
    return len(split_text)

    

def function_get_response(query):

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 2, "lambda_mult": 0.5}
    )
    context = retriever.invoke(query)

    prompt = f"""Answer the question using ONLY the context below.
               If the answer is not present, say "I don't know".

            Context:
            {context}
            
            Question:
            {query}
         """
    
    response = llm.invoke(prompt);
    return {
        "answer": response.content,
    }
  



