from huey.contrib.djhuey import task

from documents.models import Document
from documents.methods import process_ocr, summarize_document, process_vector

# import json


@task()
def process_document(document: Document):
    ocr_content = process_ocr(document)
    summarize_document(document, ocr_content)
    process_vector(document, ocr_content)
