from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from vector_store import create_vector_store

INPUT_MD_FILE = "output.md"

with open(INPUT_MD_FILE, "r", encoding="utf-8") as f:
    markdown_document = f.read()

headers_to_split_on = [
    ("#", "heading_1"),
    ("##", "heading_2"),
    ("###", "heading_3"),
]

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on, strip_headers=False
)
md_header_splits = markdown_splitter.split_text(markdown_document)

chunk_size = 250
chunk_overlap = 30
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap
)

docs = text_splitter.split_documents(md_header_splits)
create_vector_store(docs)
print(f"✅ Successfully added {len(docs)} documents.")