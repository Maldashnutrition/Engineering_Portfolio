#!/usr/bin/env python3
"""
Library Management System – CLI Wrapper
Simplified version using executescript() for reliability.
"""

import sys
import os
import sqlite3
from pathlib import Path

DB_PATH = Path("library.db")
SCHEMA_PATH = Path("schema.sql")
SEED_PATH = Path("seed.sql")

def init_database():
    if not SCHEMA_PATH.exists():
        print(f"Error: Schema file not found: {SCHEMA_PATH}")
        return False

    print("Initializing database...")
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.executescript(SCHEMA_PATH.read_text(encoding='utf-8'))
        conn.commit()
        conn.close()
        print("✅ Database schema created successfully.")
        return True
    except sqlite3.Error as e:
        print(f"❌ Error creating schema: {e}")
        return False

def seed_database():
    if not SEED_PATH.exists():
        print(f"Error: Seed file not found: {SEED_PATH}")
        return False

    print("Loading sample data...")
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.executescript(SEED_PATH.read_text(encoding='utf-8'))
        conn.commit()
        conn.close()
        print("✅ Sample data loaded successfully.")
        return True
    except sqlite3.Error as e:
        print(f"❌ Error loading seed data: {e}")
        return False

def reset_database():
    if DB_PATH.exists():
        print(f"Removing existing database...")
        os.remove(DB_PATH)
    if init_database():
        seed_database()

def run_query(sql):
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if cursor.description:
            headers = [desc[0] for desc in cursor.description]
            print(" | ".join(headers))
            print("-" * len(" | ".join(headers)))
            for row in rows:
                print(" | ".join(str(val) for val in row))
        else:
            print("Query executed successfully.")
        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

def interactive():
    print("Library Management System – Interactive Mode")
    print("Type SQL queries (end with a semicolon) or 'exit' to quit.")
    while True:
        sql = input("sql> ").strip()
        if sql.lower() == 'exit':
            break
        if not sql:
            continue
        run_query(sql)

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("Commands: init, seed, reset, query <SQL>, interactive")
        return

    cmd = sys.argv[1].lower()
    if cmd == "init":
        init_database()
    elif cmd == "seed":
        seed_database()
    elif cmd == "reset":
        reset_database()
    elif cmd == "query":
        if len(sys.argv) < 3:
            print("Please provide SQL query.")
            return
        run_query(" ".join(sys.argv[2:]))
    elif cmd == "interactive":
        interactive()
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
