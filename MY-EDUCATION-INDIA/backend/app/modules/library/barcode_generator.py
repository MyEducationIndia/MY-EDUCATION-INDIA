"""
Module 14: Accession Barcode Generator
"""
import hashlib

def generate_accession_barcode(institute_id: str, sequence_num: int) -> str:
    inst_hash = hashlib.sha256(institute_id.encode("utf-8")).hexdigest()[:4].upper()
    return f"ACC-{inst_hash}-{sequence_num:06d}"
