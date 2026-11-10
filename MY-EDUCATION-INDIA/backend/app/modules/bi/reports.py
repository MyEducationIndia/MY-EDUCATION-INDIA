"""
Module 18: Ready-made Institutional Report Templates
"""
def get_prebuilt_templates():
    return [
        {"code": "REP_ADM_01", "name": "Monthly Admissions & Conversion Ledger", "category": "ADMISSION"},
        {"code": "REP_FEE_01", "name": "Institutional Fee Dues & Aging Register", "category": "FINANCIAL"},
        {"code": "REP_ATT_01", "name": "Student Attendance Threshold Audit (<75%)", "category": "ATTENDANCE"},
        {"code": "REP_EXM_01", "name": "End-Term Result Merit & Grade Distribution", "category": "EXAM"}
    ]
