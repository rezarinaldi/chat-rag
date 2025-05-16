from django.shortcuts import render, redirect
from django.views import View
from .models import Document
from .tasks import process_document
from core.ai.chromadb import chroma, openai_ef


class DocumentUploadView(View):
    def get(self, request):
        return render(request, "documents/index.html")

    def post(self, request):
        file = request.FILES.get("file")

        try:
            document = Document.objects.create(file=file, name=file.name)
            process_document(document)

        except Exception as e:
            print(e)

        return redirect("documents")


class QueryView(View):
    def get(self, request):
        return render(request, "documents/query.html")

    def post(self, request):
        query = request.POST.get("query")

        collection = chroma.get_collection(
            name="6826afeea7a80a05509ee4a7", embedding_function=openai_ef
        )
        data = collection.query(
            query_texts=[query],
            n_results=3,
        )

        print(data)
