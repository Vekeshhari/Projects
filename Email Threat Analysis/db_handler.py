# db_handler.py
import pymysql
from config import DB_CONFIG
from datetime import datetime


def connect_db():
    """Connect to the MySQL database."""
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        print("❌ Database connection failed:", e)
        return None

def insert_trusted(email_id, time_received=None):
    conn = connect_db()
    if conn:
        try:
            time_received = time_received or datetime.now()
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO trusted (email_id, time_received) VALUES (%s, %s)", (email_id, time_received))
                conn.commit()
        except Exception as e:
            print("❌ Failed to insert into trusted:", e)
        finally:
            conn.close()

def insert_untrusted(email_id, term, time_received=None):
    conn = connect_db()
    if conn:
        try:
            time_received = time_received or datetime.now()
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO untrusted (email_id, suspicious_term, time_received) VALUES (%s, %s, %s)", (email_id, term, time_received))
                conn.commit()
        except Exception as e:
            print("❌ Failed to insert into untrusted:", e)
        finally:
            conn.close()

def insert_email_hash(email_id, email_hash, time_received):
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO email_hash (email_id, email_hash, time_received) VALUES (%s, %s, %s)",
                    (email_id, email_hash, time_received)
                )
                conn.commit()
        except Exception as e:
            print("❌ Failed to insert into email_hash:", e)
        finally:
            conn.close()

def get_all_emails():
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT email_id FROM email_hash")
                results = [row[0] for row in cursor.fetchall()]
                return results
        except Exception as e:
            print("❌ Failed to fetch emails:", e)
        finally:
            conn.close()
    return []

def insert_not_spoofed(email_id, time_received=None):
    """Insert a verified non-spoofed email into the not_spoofed table."""
    conn = connect_db()
    if conn:
        try:
            time_received = time_received or datetime.now()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT IGNORE INTO not_spoofed (email_id, time_received) VALUES (%s, %s)", (email_id, time_received)
                )
                conn.commit()
        except Exception as e:
            print("❌ Failed to insert into not_spoofed:", e)
        finally:
            conn.close()

def get_not_spoofed_emails():
    """Retrieve all email addresses marked as not spoofed."""
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT email_id FROM not_spoofed")
                result = cursor.fetchall()
                return [row[0] for row in result]
        except Exception as e:
            print("❌ Failed to fetch from not_spoofed:", e)
        finally:
            conn.close()
    return []

def insert_spoofed(email_id, time_received=None):
    """Insert a spoofed email into the spoofed table."""
    conn = connect_db()
    if conn:
        try:
            time_received = time_received or datetime.now()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO spoofed (mail, time_received) VALUES (%s, %s)",
                    (email_id, time_received)
                )
                conn.commit()
        except Exception as e:
            print("❌ Failed to insert into spoofed:", e)
        finally:
            conn.close()


def insert_link_file(email_id, link_url, time_received):
    """Insert an email with a link into the link_files table."""
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO link_files (email_id, url, time_received) VALUES (%s, %s, %s)",
                    (email_id, link_url, time_received)
                )
                conn.commit()
        except Exception as e:
            print("❌ Failed to insert into link_files:", e)
        finally:
            conn.close()
