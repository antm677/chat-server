import os
from google.cloud import storage
from vertexai.preview.generative_models import GenerativeModel, Part

BUCKET_NAME = "rjs-influencemeter.appspot.com"
INPUT_FOLDER = "source_pdf"
DESTINATION_BLOB_NAME = "uploaded/input.pdf"
LOCAL_PDF_PATH = "input.pdf"
PROJECT_ID = "rjs-influencemeter"
REGION = "us-central1"
OUTPUT_MD_PATH = "output.md"
UPLOAD_PREFIX = "uploaded"


def upload_to_gcs(bucket_name, source_file_path, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)
    gcs_uri = f"gs://{bucket_name}/{destination_blob_name}"
    print(f"✅ Uploaded {source_file_path} to {gcs_uri}")
    return gcs_uri


def extract_pdf_with_vertex_ai(gcs_uri):
    model = GenerativeModel("gemini-2.0-flash-lite")
    file_part = Part.from_uri(gcs_uri, mime_type="application/pdf")

    prompt = "Extract the content from this PDF and convert it into well-formatted Markdown."
    response = model.generate_content([prompt, file_part])

    return response.text


def append_markdown_to_file(markdown_text, output_path, file_label):
    with open(output_path, "a", encoding="utf-8") as f:
        f.write(markdown_text)
    print(f"📄 Appended Markdown for {file_label} to {output_path}")


def main():
    pdf_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("❌ No PDF files found.")
        return

    open(OUTPUT_MD_PATH, "w").close()

    for filename in pdf_files:
        local_pdf_path = os.path.join(INPUT_FOLDER, filename)
        blob_name = f"{UPLOAD_PREFIX}/{filename}"

        try:
            gcs_uri = upload_to_gcs(BUCKET_NAME, local_pdf_path, blob_name)
            markdown = extract_pdf_with_vertex_ai(gcs_uri)
            append_markdown_to_file(markdown, OUTPUT_MD_PATH, filename)
        except Exception as e:
            print(f"⚠️ Failed to process {filename}: {e}")

if __name__ == "__main__":
    main()



