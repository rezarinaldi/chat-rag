from core.ai.mistral import mistral
from core.methods import send_notification
from documents.models import Document, DOC_PROCESS_DONE
from core.ai.prompt_manager import PromptManager
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import OpenAIEmbeddings
from core.ai.chromadb import chroma, openai_ef


def process_ocr(document: Document):
    send_notification("notification", "Processing document...")
    uploaded_pdf = mistral.files.upload(
        file={
            "file_name": document.name,
            "content": open(f"media/{document.file.name}", "rb"),
        },
        purpose="ocr",
    )

    signed_url = mistral.files.get_signed_url(file_id=uploaded_pdf.id)
    print(signed_url)

    ocr_result = mistral.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "document_url", "document_url": signed_url.url},
    )

    content = ""

    for page in ocr_result.dict().get("pages", []):
        content += page["markdown"]


def summarize_document(document: Document, text: str):
    send_notification("notification", "Summarizing document...")
    pm = PromptManager(model="gpt-4.1")
    pm.add_message(
        "system", "Please summarize the provided text. Extract also the key points."
    )
    pm.add_message("user", f"Content: {text}")

    summarized_content = pm.generate()

    document.raw_text = text
    document.summary_text = summarized_content
    document.status = DOC_PROCESS_DONE
    document.save()


def process_vector(document: Document, text: str):
    send_notification("notification", "Creating document...")

    splitter = SemanticChunker(OpenAIEmbeddings())
    documents = splitter.create_documents([text])

    collection = chroma.create_collection(
        name=document.id, embedding_function=openai_ef
    )
    collection.add(
        documents=[doc.model_dump().get("page_content") for doc in documents],
        ids=[str(i) for i in range(len(documents))],
    )

    send_notification("done", "Document processed successfully!")
