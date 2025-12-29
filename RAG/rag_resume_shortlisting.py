import streamlit as st
import os
import tempfile
import re
import chromadb

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import init_embeddings


st.set_page_config(page_title="AI Resume Shortlisting", layout="wide")
st.title("📄 AI Enabled Resume Shortlisting System")
st.write("Upload, manage, and shortlist resumes using AI embeddings & RAG")


embed_model = init_embeddings(
    model="text-embedding-all-minilm-l6-v2-embedding",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1/embeddings",
    api_key="not-needed",
    check_embedding_ctx_length=False
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20,
    separators=[" ", "\n", "\n\n"]
)


db = chromadb.PersistentClient(path="./knowledge_base")
collection = db.get_or_create_collection(name="resumes")


def load_pdf_resume(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    full_text = "\n".join([p.page_content for p in pages])
    return full_text, len(pages)


def store_or_update_resume(pdf_path, resume_id):
    all_ids = collection.get()["ids"]
    delete_ids = [i for i in all_ids if i.startswith(resume_id)]
    if delete_ids:
        collection.delete(ids=delete_ids)

    text, page_count = load_pdf_resume(pdf_path)
    file_name = os.path.basename(pdf_path)

    docs = text_splitter.create_documents(
        texts=[text],
        metadatas=[{"resume_id": resume_id, "file_name": file_name, "page_count": page_count}]
    )

    texts, metadatas, ids = [], [], []
    for i, doc in enumerate(docs):
        texts.append(doc.page_content)
        metadatas.append(doc.metadata)
        ids.append(f"{resume_id}_chunk_{i}")

    embeddings = embed_model.embed_documents(texts)
    collection.add(ids=ids, documents=texts, metadatas=metadatas, embeddings=embeddings)


def delete_resume(resume_id):
    all_ids = collection.get()["ids"]
    delete_ids = [i for i in all_ids if i.startswith(resume_id)]
    if delete_ids:
        collection.delete(ids=delete_ids)


def list_resumes():
    metadatas = collection.get()["metadatas"]
    if not metadatas:
        return {}
    unique = {}
    for meta in metadatas:
        rid = meta["resume_id"]
        if rid not in unique:
            unique[rid] = {"file_name": meta["file_name"], "page_count": meta["page_count"]}
    return unique


def shortlist_resumes(job_desc, top_k):
    jd_embedding = embed_model.embed_documents([job_desc])[0]
    results = collection.query(query_embeddings=[jd_embedding], n_results=top_k)
    shortlisted = list({meta["resume_id"] for meta in results["metadatas"][0]})
    return shortlisted

def extract_candidate_info(pdf_text):
    lines = [l.strip() for l in pdf_text.split("\n") if l.strip()]
    name = lines[0] if lines else "N/A"

    phone_match = re.search(r"\+?\d[\d\s\-]{7,}\d", pdf_text)
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", pdf_text)
    contact = ""
    if phone_match: contact += phone_match.group()
    if email_match: contact += f" | {email_match.group()}" if contact else email_match.group()
    if not contact: contact = "N/A"

    skills = "N/A"
    skills_match = re.search(r"(Skills|Technical Skills|Expertise)[:\n](.*)", pdf_text, re.I)
    if skills_match:
        skills = skills_match.group(2).strip().split("\n")[0]

    exp_match = re.search(r"(\d+\+?\s*(years|yrs))", pdf_text, re.I)
    experience = exp_match.group(1) if exp_match else "N/A"

    return name, contact, skills, experience

tab1, tab2, tab3, tab4 = st.tabs(
    ["📤 Upload Resume", "📋 List Resumes", "🗑️ Delete Resume", "⭐ Shortlist"]
)

with tab1:
    st.subheader("Upload Resume")
    col1, col2 = st.columns([2, 3])
    with col1:
        resume_id = st.text_input("Resume ID (e.g., 001, JohnDoe)")
    with col2:
        uploaded_file = st.file_uploader("Choose PDF file", type=["pdf"])

    if uploaded_file and resume_id:
        if st.button("Upload Resume"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                pdf_path = tmp.name
            store_or_update_resume(pdf_path, resume_id)
            st.success(f"✅ Resume uploaded successfully: {resume_id}")


with tab2:
    st.subheader("Resumes in Database")
    resumes = list_resumes()
    if resumes:
        for r_id, meta in resumes.items():
            st.info(f"{r_id} | {meta['file_name']} | Pages: {meta['page_count']}")
    else:
        st.warning("No resumes found")


with tab3:
    st.subheader("Delete Resume")
    resumes = list_resumes()
    if resumes:
        selected = st.selectbox("Select resume to delete", list(resumes.keys()))
        if st.button("Delete Resume"):
            delete_resume(selected)
            st.success("🗑️ Resume deleted successfully")
    else:
        st.warning("No resumes available to delete")


with tab4:
    st.subheader("Shortlist Resumes for Job Description")
    job_desc = st.text_area("Enter Job Description")
    top_k = st.number_input("Number of resumes to shortlist", 1, 10, 3)

    if st.button("Shortlist Resumes"):
        shortlisted_ids = shortlist_resumes(job_desc, top_k)
        if shortlisted_ids:
            for r_id in shortlisted_ids:
                doc_ids = [i for i in collection.get()["ids"] if i.startswith(r_id)]
                if doc_ids:
                    pdf_text = " ".join(collection.get(ids=[doc_ids[0]])["documents"])
                    name, contact, skills, experience = extract_candidate_info(pdf_text)
                    with st.expander(f"ID: {r_id} | {name}"):
                        st.write(f"📞 Contact: {contact}")
                        st.write(f"💼 Experience: {experience}")
                        st.write(f"🛠 Skills: {skills}")
        else:
            st.warning("No resumes matched the job description")
