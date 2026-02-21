import os
import sqlite3
import json
import hmac
import hashlib
from cryptography.fernet import Fernet
import streamlit as st


# 1. Key Management

KEY_FILE = "secret.key"

def load_or_generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key

MASTER_KEY = load_or_generate_key()
cipher = Fernet(MASTER_KEY)

# 1.5 Salt for HMAC (to prevent rainbow table attacks on trapdoors)
#  HMAC (can be stored in code or env variable)

SALT_FILE = "salt.bin"

def load_or_generate_salt():
    if not os.path.exists(SALT_FILE):
        salt = os.urandom(16)  # 128-bit salt
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
    else:
        with open(SALT_FILE, "rb") as f:
            salt = f.read()
    return salt

SALT = load_or_generate_salt()

# 2. Secure Trapdoor (HMAC-based)

def generate_trapdoor(word: str) -> str:
    """
    Salted HMAC-based trapdoor.
    Deterministic but protected against rainbow-table attacks.
    """

    normalized = word.lower().strip().encode()

    # Combine salt + word before HMAC
    salted_word = SALT + normalized

    return hmac.new(MASTER_KEY, salted_word, hashlib.sha256).hexdigest()


# 3. Database Initialization

def init_db():
    conn = sqlite3.connect("securevault.db")
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


# 4. Insert Encrypted Record

def insert_record(conn, record: dict):
    cursor = conn.cursor()

    acc_no = record["acc_no"]

    # Encrypt entire record
    encrypted_blob = cipher.encrypt(json.dumps(record).encode())

    try:
        cursor.execute(
            "INSERT INTO data_store (acc_no, payload) VALUES (?, ?)",
            (acc_no, encrypted_blob)
        )
    except sqlite3.IntegrityError:
        st.error("Account number already exists!")
        return

    # Index searchable fields
    terms = record["name"].split() + [record["acc_no"]]

    for term in set(terms):
        trapdoor = generate_trapdoor(term)
        cursor.execute(
            "INSERT INTO search_index (trapdoor, acc_no) VALUES (?, ?)",
            (trapdoor, acc_no)
        )

    conn.commit()


# 5. Secure Search

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
        decrypted = cipher.decrypt(row[0])
        results.append(json.loads(decrypted.decode()))

    return results


# 6. Streamlit UI

st.set_page_config(page_title="SecureVault", layout="wide")
st.title("SecureVault - Searchable Encryption System")

conn = init_db()

# Sample data
customers = [
    {"name": "Aarav Sharma", "acc_no": "20001", "balance": "7500"},
    {"name": "Diya Patel", "acc_no": "20002", "balance": "12000"},
    {"name": "Rohan Mehta", "acc_no": "20003", "balance": "5600"},
    {"name": "Ananya Iyer", "acc_no": "20004", "balance": "9800"},
    {"name": "Kabir Singh", "acc_no": "20005", "balance": "1500"},
    {"name": "Meera Nair", "acc_no": "20006", "balance": "6400"},
    {"name": "Arjun Reddy", "acc_no": "20007", "balance": "22000"},
    {"name": "Sneha Kulkarni", "acc_no": "20008", "balance": "3400"},
    {"name": "Vikram Rao", "acc_no": "20009", "balance": "8800"},
    {"name": "Ishita Verma", "acc_no": "20010", "balance": "4300"},
    {"name": "Rahul Das", "acc_no": "20011", "balance": "17000"},
    {"name": "Pooja Menon", "acc_no": "20012", "balance": "3900"},
    {"name": "Nikhil Jain", "acc_no": "20013", "balance": "8100"},
    {"name": "Kavya Shetty", "acc_no": "20014", "balance": "2600"},
    {"name": "Aditya Kapoor", "acc_no": "20015", "balance": "9900"},
    {"name": "Tanya Bhat", "acc_no": "20016", "balance": "5400"},
    {"name": "Siddharth Malhotra", "acc_no": "20017", "balance": "12500"},
    {"name": "Neha Agarwal", "acc_no": "20018", "balance": "7100"},
    {"name": "Yash Thakur", "acc_no": "20019", "balance": "600"},
    {"name": "Ritika Sinha", "acc_no": "20020", "balance": "14300"},
    {"name": "Manish Choudhary", "acc_no": "20021", "balance": "4700"},
    {"name": "Shruti Desai", "acc_no": "20022", "balance": "8300"},
    {"name": "Karan Oberoi", "acc_no": "20023", "balance": "11200"},
    {"name": "Bhavna Rao", "acc_no": "20024", "balance": "2900"},
    {"name": "Harsh Vardhan", "acc_no": "20025", "balance": "5200"},
    {"name": "Divya Joshi", "acc_no": "20026", "balance": "4600"},
    {"name": "Pranav Kulkarni", "acc_no": "20027", "balance": "15000"},
    {"name": "Aishwarya Pillai", "acc_no": "20028", "balance": "9200"},
    {"name": "Gaurav Mishra", "acc_no": "20029", "balance": "6800"},
    {"name": "Sanya Kapoor", "acc_no": "20030", "balance": "10400"}
]

def preload_data(conn):
    for record in customers:
        insert_record(conn, record)

if st.sidebar.button("Load Demo Data (30 Records)"):
    preload_data(conn)
    st.sidebar.success("30 demo records securely inserted!")

st.sidebar.header("Add Record")

name = st.sidebar.text_input("Customer Name")
acc_no = st.sidebar.text_input("Account Number")
balance = st.sidebar.text_input("Balance")

if st.sidebar.button("Store Securely"):
    if name and acc_no and balance:
        record = {
            "name": name,
            "acc_no": acc_no,
            "balance": balance
        }
        insert_record(conn, record)
        st.sidebar.success("Record encrypted and stored securely!")
    else:
        st.sidebar.warning("All fields required.")

st.header("Secure Search")

search_term = st.text_input("Enter Name or Account Number")

if st.button("Search"):
    if search_term:
        results = search_records(conn, search_term)

        if results:
            st.success(f"{len(results)} match(es) found.")
            for r in results:
                st.json(r)
        else:
            st.error("No matches found.")
    else:
        st.warning("Enter search term.")
