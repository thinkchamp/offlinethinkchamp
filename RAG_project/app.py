from flask import Flask, render_template, request
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Transformer Model
model = SentenceTransformer('all-MiniLM-L6-v2')

documents = []
index = None


@app.route("/", methods=["GET", "POST"])
def home():
    global documents, index

    answer = ""

    if request.method == "POST":

        # =====================
        # PDF Upload
        # =====================
        if "pdf" in request.files:

            pdf = request.files["pdf"]

            if pdf.filename != "":

                path = os.path.join(
                    UPLOAD_FOLDER,
                    pdf.filename
                )

                pdf.save(path)

                try:
                    reader = PdfReader(path)

                    text = ""

                    for page in reader.pages:

                        page_text = page.extract_text()

                        if page_text:
                            text += page_text + "\n"

                    # =====================
                    # Chunking
                    # =====================

                    documents = []

                    for line in text.split("\n"):

                        line = line.strip()

                        if len(line) > 0:
                            documents.append(line)

                    print("\nDOCUMENTS:")
                    for doc in documents:
                        print(doc)

                    # =====================
                    # Embeddings
                    # =====================

                    vectors = model.encode(documents)

                    vectors = np.array(
                        vectors,
                        dtype=np.float32
                    )

                    # =====================
                    # FAISS Index
                    # =====================

                    dimension = vectors.shape[1]

                    index = faiss.IndexFlatL2(
                        dimension
                    )

                    index.add(vectors)

                    answer = (
                        f"PDF Uploaded Successfully. "
                        f"{len(documents)} chunks created."
                    )

                except Exception as e:

                    answer = f"PDF Error: {e}"

        # =====================
        # Ask Question
        # =====================
        elif "question" in request.form:

            if index is None:

                answer = (
                    "Please upload a PDF first."
                )

            else:

                question = request.form[
                    "question"
                ]

                query_vector = model.encode(
                    [question]
                )

                query_vector = np.array(
                    query_vector,
                    dtype=np.float32
                )

                distances, results = index.search(
                    query_vector,
                    k=1
                )

                best_match = results[0][0]

                answer = documents[
                    best_match
                ]

                print("\nQUESTION:")
                print(question)

                print("\nANSWER:")
                print(answer)

    return render_template(
        "index.html",
        answer=answer
    )


if __name__ == "__main__":
    app.run(debug=True)