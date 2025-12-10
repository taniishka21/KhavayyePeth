# staybite/core/chatbot_app.py

from __future__ import annotations
import os, json
from typing import List, Dict
from pathlib import Path
import numpy as np
import pandas as pd
from django.conf import settings
import google.generativeai as genai
from dotenv import load_dotenv

# ---------- Config ----------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

DATA_PATH = settings.BASE_DIR / "core" / "data" / "zomato_outlet_final.csv"
EMB_PATH = settings.BASE_DIR / "core" / "data" / "zomato_embeds.npy"
MODEL_CHAT = "gemini-1.5-flash"
MODEL_EMB = "models/embedding-001"
TOP_K = 12
DISPLAY_K = 5

# Initialize models
chat_model = genai.GenerativeModel(MODEL_CHAT)

# ---------- Load dataset ----------
def load_df() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"CSV not found at {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.lower()
    rename_map = {
        "rest_name": "name",
        "rest_type": "type",
        "loc": "location",
        "dine_rating": "rating_dine",
        "delivery_rating": "rating_delivery",
        "cuisine": "cuisines",
        "cost": "cost",
        "liked": "highlights"
    }
    df = df.rename(columns=rename_map)

    for col in ["name", "type", "location", "cuisines", "highlights"]:
        if col not in df: df[col] = ""
        df[col] = df[col].astype(str).fillna("").str.strip()

    for col in ["rating_dine", "rating_delivery", "cost"]:
        if col not in df: df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["text"] = (
        df["name"].fillna("") + " | " +
        df["type"].fillna("") + " | " +
        df["location"].fillna("") + " | " +
        df["cuisines"].fillna("") + " | " +
        df["highlights"].fillna("") + " | " +
        df["rating_dine"].fillna(0).astype(str) + " | " +
        df["rating_delivery"].fillna(0).astype(str) + " | " +
        df["cost"].fillna(0).astype(int).astype(str)
    )
    return df.reset_index(drop=True)

DF = load_df()

# ---------- Embeddings ----------
def embed_texts(texts: List[str], task_type: str):
    """Generates embeddings for a list of texts using the Gemini API."""
    if not isinstance(texts, list):
        texts = [texts]
    result = genai.embed_content(
        model=MODEL_EMB,
        content=texts,
        task_type=task_type
    )
    return np.array(result["embedding"])

def load_or_create_embeddings():
    if EMB_PATH.exists():
        print("Loading pre-computed embeddings...")
        return np.load(EMB_PATH)
    else:
        print("Creating embeddings for the first time...")
        df_texts = DF["text"].tolist()
        embeddings = []
        batch_size = 100
        for i in range(0, len(df_texts), batch_size):
            batch = df_texts[i:i+batch_size]
            embeddings.extend(embed_texts(batch, task_type="RETRIEVAL_DOCUMENT"))
        
        embeddings = np.array(embeddings)
        np.save(EMB_PATH, embeddings)
        print("Embeddings saved to", EMB_PATH)
        return embeddings

EMB = load_or_create_embeddings()

# ---------- Semantic search ----------
def search_rows(query: str, top_k: int = TOP_K) -> pd.DataFrame:
    if not query.strip():
        return DF.sort_values(by=["rating_dine"], ascending=False).head(top_k)

    try:
        q_emb = embed_texts(query, task_type="RETRIEVAL_QUERY")[0]
        
        sims = EMB @ q_emb
        top_k_safe = min(top_k, len(sims))
        idx = np.argpartition(-sims, top_k_safe)[:top_k_safe]
        
        top = DF.iloc[idx].copy()
        top["score"] = sims[idx]
        return top.sort_values("score", ascending=False)
        
    except Exception as e:
        print(f"Search failed: {e}")
        return pd.DataFrame() # Return an empty DataFrame on error

# ---------- Format context ----------
def format_context(rows: pd.DataFrame, limit: int = DISPLAY_K) -> str:
    if rows.empty:
        return "[]"

    rows = rows.head(limit)
    lines = []
    for _, r in rows.iterrows():
        line = {
            "name": r["name"],
            "type": r["type"],
            "location": r["location"],
            "cuisines": r["cuisines"],
            "dine_rating": None if pd.isna(r["rating_dine"]) else round(float(r["rating_dine"]), 1),
            "delivery_rating": None if pd.isna(r["rating_delivery"]) else round(float(r["rating_delivery"]), 1),
            "cost": None if pd.isna(r["cost"]) else int(r["cost"]),
            "highlights": r["highlights"]
        }
        lines.append(line)
    return json.dumps(lines, ensure_ascii=False, indent=2)

SYSTEM_PROMPT = (
    "You are Khavayye AI, a helpful Pune food guide.\n"
    "You MUST only use the provided 'dataset_context' to answer.\n"
    "If the context is empty, ask the user a clarifying question (area, cuisine, budget).\n"
    "Answer in short, helpful bullet points with: name, type, area, cuisine, dine rating, delivery rating, approx cost, and highlights.\n"
    "Do not hallucinate restaurants not in the context."
)

# ---------- Gemini Answer ----------
def answer_with_dataset(query: str, history: List[Dict]) -> str:
    # Use the full history to make a better search query
    full_query = " ".join([m['text'] for m in history if m['role'] == 'user'])
    top = search_rows(full_query, top_k=TOP_K)
    
    if top.empty:
        context_json = "[]"
    else:
        context_json = format_context(top, limit=DISPLAY_K)

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"User query: {query}\n\n"
        f"dataset_context (JSON array of restaurants):\n{context_json}\n\n"
        "Write the answer ONLY based on dataset_context."
    )
    
    response = chat_model.generate_content(prompt)
    return response.text.strip()

# ---------- Public API ----------
def chatbot_api(user_msg: str, history: List[Dict]) -> str:
    try:
        return answer_with_dataset(user_msg or "", history)
    except Exception as e:
        return f"Sorry, I hit an error. Please try again. (details: {str(e)[:120]})"