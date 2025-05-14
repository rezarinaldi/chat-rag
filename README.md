## Build App Chat RAG

### Guide

```bash
python -m venv .venv
```

For Windows, bisa pakai Git Bash,

```bash
source .venv/Scripts/activate
```

For Mac,

```bash
source .venv/bin/activate
```

```bash
pip install openai python-dotenv
```

```bash
pip install chromadb mistralai
```

Menjalankan ChromaDB, kemudian ganti port menjadi `8010`

```bash
chroma run --path data --port 8010
```

```bash
pip install langchain_experimental langchain_openai
```

```bash
pip freeze > requirements.txt
```

Jika sudah ada ada file requirements.txt, kita bisa menjalankan perintah ini,

```bash
pip install -r requirements.txt
```

### Source

- [OpenAI](https://pypi.org/project/openai/)
- [ChromaDB](https://docs.trychroma.com/docs/overview/introduction)
- [MistralAI](https://mistral.ai/)
- [LangChain](https://python.langchain.com/docs/how_to/semantic-chunker/)
