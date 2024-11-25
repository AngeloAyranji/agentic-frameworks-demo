from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

def split_transcript_into_chunks(transcript, chunk_size=1200, chunk_overlap=200):
    """
    Splits a transcript into chunks of up to `chunk_size` tokens.
    
    Args:
        transcript (str): The full transcript text.
        max_tokens (int): Maximum number of tokens per chunk.

    Returns:
        list: A list of transcript chunks.
    """
    doc = Document(page_content=transcript)
        
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
        
    chunks = text_splitter.split_documents([doc])

    return chunks

def summarize_chunk(chunk):
    """
    Creates a concise summary of a document chunk using LangChain and OpenAI.
    
    Args:
        chunk (str): The text to summarize.
        
    Returns:
        SummaryFormatter: A structured output containing the summary and importance flag
    """

    class SummaryFormatter(BaseModel):
        summary: str = Field(description="A concise summary of the text")
        isImportant: bool = Field(description="Whether the summary contains important information that should be added to the database")

    model = ChatOpenAI(model="gpt-4", temperature=0.3)
    
    prompt = ChatPromptTemplate.from_template(
        "You are a startup assistant that helps founders build their companies. "
        "Extract the key points and important details from the following text. "
        "Talk in the second person. "
        "Keep the summary brief but informative.\n\n"
        "Text: {text}"
    )
    
    model_with_structured_output = model.with_structured_output(SummaryFormatter)
    chain = prompt | model_with_structured_output
    
    response = chain.invoke({"text": chunk})
    return response