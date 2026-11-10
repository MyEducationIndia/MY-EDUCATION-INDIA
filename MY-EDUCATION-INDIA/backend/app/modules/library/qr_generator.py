"""
Module 14: QR Generator for Book Copies & Accession
"""
import json

def generate_book_copy_qr_payload(accession_num: str, title: str, isbn: str) -> str:
    return json.dumps({
        "accession": accession_num,
        "title": title[:50],
        "isbn": isbn,
        "type": "LIBRARY_BOOK_COPY"
    })
