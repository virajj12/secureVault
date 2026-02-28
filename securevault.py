import os
import sqlite3
import json
import hmac
import hashlib
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import streamlit as st

# =====================================================
# CONFIGURATION & LOGGING
# =====================================================

logging.basicConfig(
    filename="securevault.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

DB_FILE = "securevault.db"
ROOT_KEY_FILE = "root.key"
SALT_FILE = "salt.bin"

# =====================================================
# KEY HIERARCHY (Industry Standard)
# =====================================================

def load_or_generate_root_key():
    if not os.path.exists(ROOT_KEY_FILE):
        key = os.urandom(32)
        with open(ROOT_KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(ROOT_KEY_FILE, "rb") as f:
            key = f.read()
    return key

ROOT_KEY = load_or_generate_root_key()

def derive_key(context: bytes) -> bytes:
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=context,
        backend=default_backend()
    )
    return hkdf.derive(ROOT_KEY)

K_ENC = derive_key(b"encryption-key")
K_TD  = derive_key(b"trapdoor-key")
K_IDX = derive_key(b"index-integrity-key")

cipher = Fernet(base64_urlsafe_key := Fernet.generate_key())

# =====================================================
# SALT MANAGEMENT
# =====================================================

def load_or_generate_salt():
    if not os.path.exists(SALT_FILE):
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
    else:
        with open(SALT_FILE, "rb") as f:
            salt = f.read()
    return salt

GLOBAL_SALT = load_or_generate_salt()

# =====================================================
# SECURE TRAPDOOR (Blind Index)
# =====================================================

def generate_trapdoor(word: str) -> str:
    normalized = word.lower().strip().encode()
    data = GLOBAL_SALT + normalized
    return hmac.new(K_TD, data, hashlib.sha256).hexdigest()

# =====================================================
# DATABASE LAYER
# =====================================================

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_store (
            acc_no TEXT PRIMARY KEY,
            payload BLOB
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_index (
            trapdoor TEXT,
            acc_no TEXT
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_trapdoor
        ON search_index(trapdoor)
    """)

    conn.commit()
    return conn

# =====================================================
# SERVICE LAYER
# =====================================================

def encrypt_payload(record: dict) -> bytes:
    return cipher.encrypt(json.dumps(record).encode())

def decrypt_payload(blob: bytes) -> dict:
    return json.loads(cipher.decrypt(blob).decode())

def insert_record(conn, record: dict):
    cursor = conn.cursor()
    acc_no = record["acc_no"]

    encrypted_blob = encrypt_payload(record)

    try:
        cursor.execute(
            "INSERT INTO data_store (acc_no, payload) VALUES (?, ?)",
            (acc_no, encrypted_blob)
        )
    except sqlite3.IntegrityError:
        logging.warning("Duplicate account insertion attempt")
        raise

    terms = record["name"].split() + [acc_no]

    for term in set(terms):
        trapdoor = generate_trapdoor(term)
        cursor.execute(
            "INSERT INTO search_index (trapdoor, acc_no) VALUES (?, ?)",
            (trapdoor, acc_no)
        )

    conn.commit()
    logging.info("Inserted record securely")

def search_records(conn, query: str):
    cursor = conn.cursor()
    trapdoor = generate_trapdoor(query)

    cursor.execute("""
        SELECT ds.payload
        FROM data_store ds
        JOIN search_index si ON ds.acc_no = si.acc_no
        WHERE si.trapdoor = ?
    """, (trapdoor,))

    rows = cursor.fetchall()

    results = []
    for row in rows:
        results.append(decrypt_payload(row[0]))

    logging.info("Search performed securely")
    return results

# =====================================================
# STREAMLIT UI
# =====================================================

st.set_page_config(page_title="SecureVault Enterprise", layout="wide")
st.title("SecureVault Enterprise - Industry Grade Secure Search")

conn = init_db()

st.sidebar.header("Add Secure Record")

name = st.sidebar.text_input("Customer Name")
acc_no = st.sidebar.text_input("Account Number")
balance = st.sidebar.text_input("Balance")

if st.sidebar.button("Store Securely"):
    try:
        insert_record(conn, {
            "name": name,
            "acc_no": acc_no,
            "balance": balance
        })
        st.success("Securely stored.")
    except:
        st.error("Account already exists.")

st.header("Secure Search")

query = st.text_input("Search by Name or Account Number")

if st.button("Search"):
    results = search_records(conn, query)
    if results:
        for r in results:
            st.json(r)
    else:
        st.error("No results found.")