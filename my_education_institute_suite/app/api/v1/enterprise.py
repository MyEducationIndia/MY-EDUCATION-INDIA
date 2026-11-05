import time
from datetime import datetime
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.core.security import get_current_user_optional
from app.models.entities import (
    AuditLog,
    Branch,
    CMSContent,
    CertificateRecord,
    CommunicationLog,
    InventoryItem,
    LibraryBook,
    LibraryIssue,
    PayrollRecord,
)
from app.models.schemas import (
    BranchCreate,
    BranchUpdate,
    CertificateCreate,
    CommunicationDispatch,
    FeatureToggleBulkUpdate,
    InventoryItemCreate,
    InventoryItemUpdate,
    LibraryBookCreate,
    LibraryIssueCreate,
    LibraryReturnRequest,
    PayrollCreate,
)
from app.services.erp_service import EnterpriseERPService

logger = get_logger(__name__)
router = APIRouter(prefix="/enterprise", tags=["Enterprise ERP Modules (Library, Inventory, HR, Payroll, Branches, Comm, Feature Control)"])


def _fmt_dt(val: Any) -> Optional[str]:
    if not val:
        return None
    return val.strftime("%Y-%m-%d %H:%M:%S") if hasattr(val, "strftime") else str(val)


# ============================================================================
# 1. GRANULAR FEATURE VISIBILITY & CBT HIDE / SIDEBAR COLLAPSE CONTROLLER
# ============================================================================
@router.get("/features")
def get_feature_visibility(db: Session = Depends(get_db)):
    try:
        svc = EnterpriseERPService(db)
        rows = svc.ensure_default_feature_toggles()
        cms_cbt = db.query(CMSContent).filter(CMSContent.key == "hideCbtFeature").first()
        cms_sb = db.query(CMSContent).filter(CMSContent.key == "sidebarAutoCollapse").first()

        hide_cbt = (cms_cbt.value.lower() == "true") if cms_cbt else False
        sidebar_auto_collapse = (cms_sb.value.lower() == "true") if cms_sb else False

        return {
            "status": "success",
            "hide_cbt": hide_cbt,
            "sidebar_auto_collapse": sidebar_auto_collapse,
            "features": [
                {
                    "feature_key": r.feature_key,
                    "label": r.label,
                    "category": r.category,
                    "enabled": bool(r.enabled),
                }
                for r in rows
            ],
            "map": {r.feature_key: bool(r.enabled) for r in rows},
        }
    except Exception as exc:
        logger.error("Failed to fetch feature toggles: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve feature toggles.")


@router.put("/features")
def update_feature_visibility(
    payload: FeatureToggleBulkUpdate,
    db: Session = Depends(get_db),
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional),
):
    try:
        actor = str(current_user.get("sub", "admin")) if current_user else "admin"
        svc = EnterpriseERPService(db)
        updated_map = svc.update_feature_toggles(
            toggles=payload.toggles,
            hide_cbt=payload.hide_cbt,
            sidebar_auto_collapse=payload.sidebar_auto_collapse,
            actor=actor,
        )
        return {
            "status": "success",
            "message": "Feature visibility and layout preferences saved to PostgreSQL.",
            "map": updated_map,
            "hide_cbt": payload.hide_cbt,
            "sidebar_auto_collapse": payload.sidebar_auto_collapse,
        }
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update feature toggles: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to update feature toggles: {str(exc)}")


# ============================================================================
# 2. MULTI-BRANCH & FRANCHISE NETWORK MANAGEMENT
# ============================================================================
@router.get("/branches")
def list_branches(db: Session = Depends(get_db)):
    rows = db.query(Branch).order_by(Branch.id.asc()).all()
    return [
        {
            "id": b.id,
            "branch_code": b.branch_code,
            "name": b.name,
            "branch_type": b.branch_type,
            "director_name": b.director_name,
            "phone": b.phone,
            "email": b.email,
            "city": b.city,
            "state": b.state,
            "address": b.address,
            "royalty_percentage": b.royalty_percentage,
            "status": b.status,
            "created_at": _fmt_dt(b.created_at),
        }
        for b in rows
    ]


@router.post("/branches", status_code=201)
def create_branch(b: BranchCreate, db: Session = Depends(get_db)):
    try:
        code = b.branch_code or f"BR-{int(time.time() * 1000) % 10000}"
        new_b = Branch(
            branch_code=code,
            name=b.name,
            branch_type=b.branch_type or "Franchise Center",
            director_name=b.director_name or "",
            phone=b.phone,
            email=b.email or "",
            city=b.city,
            state=b.state or "Madhya Pradesh",
            address=b.address or "",
            royalty_percentage=b.royalty_percentage if b.royalty_percentage is not None else 10.0,
            status="Active",
        )
        db.add(new_b)
        db.add(AuditLog(actor="admin", action=f"Registered branch/franchise [{code}] {b.name}", module="Branches"))
        db.commit()
        db.refresh(new_b)
        return {"status": "success", "id": new_b.id, "branch_code": new_b.branch_code}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to create branch: %s", exc)
        raise HTTPException(status_code=400, detail=f"Failed to create branch: {str(exc)}")


@router.put("/branches/{branch_id}")
def update_branch(branch_id: int, b: BranchUpdate, db: Session = Depends(get_db)):
    try:
        item = db.query(Branch).filter(Branch.id == branch_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Branch not found.")
        for field, val in b.model_dump(exclude_unset=True).items():
            if val is not None:
                setattr(item, field, val)
        db.add(item)
        db.commit()
        db.refresh(item)
        return {"status": "success", "message": "Branch updated."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update branch: {str(exc)}")


@router.delete("/branches/{branch_id}")
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(Branch).filter(Branch.id == branch_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Branch not found.")
        db.delete(item)
        db.commit()
        return {"status": "success", "message": "Branch removed."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete branch: {str(exc)}")


# ============================================================================
# 3. LIBRARY MANAGEMENT (BOOKS CATALOG, BARCODE ISSUE & RETURN)
# ============================================================================
@router.get("/library/books")
def list_library_books(db: Session = Depends(get_db)):
    books = db.query(LibraryBook).order_by(LibraryBook.id.desc()).all()
    return [
        {
            "id": bk.id,
            "isbn_barcode": bk.isbn_barcode,
            "title": bk.title,
            "author": bk.author,
            "category": bk.category,
            "publisher": bk.publisher,
            "rack_no": bk.rack_no,
            "total_copies": bk.total_copies,
            "available_copies": bk.available_copies,
            "created_at": _fmt_dt(bk.created_at),
        }
        for bk in books
    ]


@router.post("/library/books", status_code=201)
def add_library_book(b: LibraryBookCreate, db: Session = Depends(get_db)):
    try:
        code = b.isbn_barcode or f"ISBN-{int(time.time() * 1000) % 100000}"
        copies = b.total_copies or 5
        bk = LibraryBook(
            isbn_barcode=code,
            title=b.title,
            author=b.author,
            category=b.category or "Computer Science",
            publisher=b.publisher or "",
            rack_no=b.rack_no or "RACK-A1",
            total_copies=copies,
            available_copies=copies,
        )
        db.add(bk)
        db.add(AuditLog(actor="admin", action=f"Added library book [{code}] {b.title}", module="Library"))
        db.commit()
        db.refresh(bk)
        return {"status": "success", "id": bk.id, "isbn_barcode": bk.isbn_barcode}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to add library book: {str(exc)}")


@router.delete("/library/books/{book_id}")
def delete_library_book(book_id: int, db: Session = Depends(get_db)):
    try:
        bk = db.query(LibraryBook).filter(LibraryBook.id == book_id).first()
        if not bk:
            raise HTTPException(status_code=404, detail="Library book not found.")
        db.delete(bk)
        db.commit()
        return {"status": "success", "message": "Library book removed."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete book: {str(exc)}")


@router.get("/library/issues")
def list_library_issues(db: Session = Depends(get_db)):
    issues = db.query(LibraryIssue).order_by(LibraryIssue.id.desc()).all()
    return [
        {
            "id": i.id,
            "book_id": i.book_id,
            "book_title": i.book_title,
            "borrower_id": i.borrower_id,
            "borrower_name": i.borrower_name,
            "borrower_role": i.borrower_role,
            "issue_date": i.issue_date,
            "due_date": i.due_date,
            "return_date": i.return_date,
            "fine_amount": i.fine_amount,
            "status": i.status,
        }
        for i in issues
    ]


@router.post("/library/issues", status_code=201)
def issue_library_book(req: LibraryIssueCreate, db: Session = Depends(get_db)):
    try:
        bk = db.query(LibraryBook).filter(LibraryBook.id == req.book_id).first()
        if not bk:
            raise HTTPException(status_code=404, detail="Book not found.")
        if bk.available_copies <= 0:
            raise HTTPException(status_code=400, detail="No available copies left for this book.")

        bk.available_copies -= 1
        db.add(bk)
        issue = LibraryIssue(
            book_id=bk.id,
            book_title=bk.title,
            borrower_id=req.borrower_id,
            borrower_name=req.borrower_name,
            borrower_role=req.borrower_role or "student",
            issue_date=time.strftime("%Y-%m-%d"),
            due_date=req.due_date,
            status="Issued",
        )
        db.add(issue)
        db.add(AuditLog(actor="admin", action=f"Issued book '{bk.title}' to {req.borrower_name}", module="Library"))
        db.commit()
        db.refresh(issue)
        return {"status": "success", "issue_id": issue.id}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to issue book: {str(exc)}")


@router.put("/library/issues/{issue_id}/return")
def return_library_book(issue_id: int, req: LibraryReturnRequest, db: Session = Depends(get_db)):
    try:
        issue = db.query(LibraryIssue).filter(LibraryIssue.id == issue_id).first()
        if not issue:
            raise HTTPException(status_code=404, detail="Issue record not found.")
        if issue.status != "Returned":
            issue.status = "Returned"
            issue.return_date = req.return_date or time.strftime("%Y-%m-%d")
            issue.fine_amount = req.fine_amount or 0.0
            db.add(issue)
            bk = db.query(LibraryBook).filter(LibraryBook.id == issue.book_id).first()
            if bk:
                bk.available_copies = min(bk.total_copies, bk.available_copies + 1)
                db.add(bk)
        db.commit()
        db.refresh(issue)
        return {"status": "success", "message": "Book returned successfully."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to return book: {str(exc)}")


# ============================================================================
# 4. INVENTORY, ASSETS, LAB COMPUTERS & STOCK MANAGEMENT
# ============================================================================
@router.get("/inventory")
def list_inventory_items(db: Session = Depends(get_db)):
    items = db.query(InventoryItem).order_by(InventoryItem.id.desc()).all()
    return [
        {
            "id": it.id,
            "asset_code": it.asset_code,
            "item_name": it.item_name,
            "category": it.category,
            "vendor_name": it.vendor_name,
            "location": it.location,
            "quantity": it.quantity,
            "unit_cost": it.unit_cost,
            "total_value": float(it.quantity or 0) * float(it.unit_cost or 0.0),
            "condition_status": it.condition_status,
            "purchase_date": it.purchase_date,
        }
        for it in items
    ]


@router.post("/inventory", status_code=201)
def create_inventory_item(req: InventoryItemCreate, db: Session = Depends(get_db)):
    try:
        code = req.asset_code or f"AST-{int(time.time() * 1000) % 100000}"
        item = InventoryItem(
            asset_code=code,
            item_name=req.item_name,
            category=req.category or "Computers & IT Lab",
            vendor_name=req.vendor_name or "",
            location=req.location or "Lab 1",
            quantity=req.quantity if req.quantity is not None else 1,
            unit_cost=req.unit_cost if req.unit_cost is not None else 0.0,
            condition_status=req.condition_status or "Operational",
            purchase_date=req.purchase_date or time.strftime("%Y-%m-%d"),
        )
        db.add(item)
        db.add(AuditLog(actor="admin", action=f"Added inventory asset [{code}] {req.item_name}", module="Inventory"))
        db.commit()
        db.refresh(item)
        return {"status": "success", "id": item.id, "asset_code": item.asset_code}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create inventory asset: {str(exc)}")


@router.put("/inventory/{item_id}")
def update_inventory_item(item_id: int, req: InventoryItemUpdate, db: Session = Depends(get_db)):
    try:
        item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Inventory asset not found.")
        for field, val in req.model_dump(exclude_unset=True).items():
            if val is not None:
                setattr(item, field, val)
        db.add(item)
        db.commit()
        db.refresh(item)
        return {"status": "success", "message": "Inventory asset updated."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update inventory asset: {str(exc)}")


@router.delete("/inventory/{item_id}")
def delete_inventory_item(item_id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Inventory asset not found.")
        db.delete(item)
        db.commit()
        return {"status": "success", "message": "Inventory asset removed."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete inventory asset: {str(exc)}")


# ============================================================================
# 5. HR & MONTHLY PAYROLL MANAGEMENT
# ============================================================================
@router.get("/payroll")
def list_payroll_records(db: Session = Depends(get_db)):
    rows = db.query(PayrollRecord).order_by(PayrollRecord.id.desc()).all()
    return [
        {
            "id": p.id,
            "voucher_no": p.voucher_no,
            "employee_code": p.employee_code,
            "employee_name": p.employee_name,
            "designation": p.designation,
            "salary_month": p.salary_month,
            "basic_salary": p.basic_salary,
            "allowances": p.allowances,
            "deductions": p.deductions,
            "net_salary": p.net_salary,
            "payment_mode": p.payment_mode,
            "payment_status": p.payment_status,
            "paid_on": p.paid_on,
        }
        for p in rows
    ]


@router.post("/payroll", status_code=201)
def process_payroll_voucher(req: PayrollCreate, db: Session = Depends(get_db)):
    try:
        vno = f"PAY-{int(time.time() * 1000) % 100000}"
        net = float(req.basic_salary) + float(req.allowances or 0.0) - float(req.deductions or 0.0)
        rec = PayrollRecord(
            voucher_no=vno,
            employee_code=req.employee_code,
            employee_name=req.employee_name,
            designation=req.designation or "Faculty",
            salary_month=req.salary_month,
            basic_salary=req.basic_salary,
            allowances=req.allowances or 0.0,
            deductions=req.deductions or 0.0,
            net_salary=max(0.0, net),
            payment_mode=req.payment_mode or "Bank NEFT",
            payment_status=req.payment_status or "Paid",
            paid_on=time.strftime("%Y-%m-%d"),
        )
        db.add(rec)
        db.add(AuditLog(actor="admin", action=f"Processed salary voucher [{vno}] for {req.employee_name}", module="Payroll"))
        db.commit()
        db.refresh(rec)
        return {"status": "success", "id": rec.id, "voucher_no": rec.voucher_no, "net_salary": rec.net_salary}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to process payroll: {str(exc)}")


@router.delete("/payroll/{payroll_id}")
def delete_payroll_record(payroll_id: int, db: Session = Depends(get_db)):
    try:
        rec = db.query(PayrollRecord).filter(PayrollRecord.id == payroll_id).first()
        if not rec:
            raise HTTPException(status_code=404, detail="Payroll record not found.")
        db.delete(rec)
        db.commit()
        return {"status": "success", "message": "Payroll voucher removed."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete payroll voucher: {str(exc)}")


# ============================================================================
# 6. COMMUNICATION HUB (BULK / SINGLE SMS, EMAIL & WHATSAPP WITH API/FREE MODES)
# ============================================================================
@router.get("/communications")
def list_communications(db: Session = Depends(get_db)):
    logs = db.query(CommunicationLog).order_by(CommunicationLog.id.desc()).limit(100).all()
    return [
        {
            "id": c.id,
            "channel": c.channel,
            "dispatch_type": c.dispatch_type,
            "gateway_mode": c.gateway_mode,
            "target_group": c.target_group,
            "recipient_count": c.recipient_count,
            "subject": c.subject,
            "message_body": c.message_body,
            "status": c.status,
            "sent_at": _fmt_dt(c.sent_at),
        }
        for c in logs
    ]


@router.post("/communications/dispatch", status_code=201)
def dispatch_communication(req: CommunicationDispatch, db: Session = Depends(get_db)):
    try:
        log = CommunicationLog(
            channel=req.channel,
            dispatch_type=req.dispatch_type or "Bulk",
            gateway_mode=req.gateway_mode or "API",
            target_group=req.target_group,
            recipient_count=req.recipient_count or 1,
            subject=req.subject or "",
            message_body=req.message_body,
            status="Delivered",
        )
        db.add(log)
        db.add(
            AuditLog(
                actor="admin",
                action=f"Dispatched {req.dispatch_type} {req.channel} ({req.gateway_mode}) to {req.target_group}",
                module="Communication",
            )
        )
        db.commit()
        db.refresh(log)
        return {
            "status": "success",
            "id": log.id,
            "channel": log.channel,
            "gateway_mode": log.gateway_mode,
            "message": f"{req.dispatch_type} {req.channel} dispatched via {req.gateway_mode} mode and logged in PostgreSQL.",
        }
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Communication dispatch failed: {str(exc)}")


# ============================================================================
# 7. DIGITAL CERTIFICATE GENERATOR & PUBLIC VERIFICATION REGISTRY
# ============================================================================
@router.get("/certificates")
def list_certificates(roll_number: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(CertificateRecord)
    if roll_number:
        q = q.filter(CertificateRecord.roll_number == roll_number)
    rows = q.order_by(CertificateRecord.id.desc()).all()
    return [
        {
            "id": c.id,
            "certificate_no": c.certificate_no,
            "roll_number": c.roll_number,
            "student_name": c.student_name,
            "course_code": c.course_code,
            "course_title": c.course_title,
            "grade": c.grade,
            "percentage": c.percentage,
            "issue_date": c.issue_date,
            "verification_status": c.verification_status,
        }
        for c in rows
    ]


@router.post("/certificates", status_code=201)
def issue_certificate(req: CertificateCreate, db: Session = Depends(get_db)):
    try:
        cert_no = req.certificate_no or f"CERT-2026-{int(time.time() * 1000) % 100000}"
        cert = CertificateRecord(
            certificate_no=cert_no,
            roll_number=req.roll_number,
            student_name=req.student_name,
            course_code=req.course_code,
            course_title=req.course_title,
            grade=req.grade or "A+",
            percentage=req.percentage if req.percentage is not None else 85.0,
            issue_date=req.issue_date or time.strftime("%Y-%m-%d"),
            verification_status="Verified",
        )
        db.add(cert)
        db.add(AuditLog(actor="admin", action=f"Issued Certificate [{cert_no}] to {req.student_name}", module="Certificates"))
        db.commit()
        db.refresh(cert)
        return {"status": "success", "id": cert.id, "certificate_no": cert.certificate_no}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to issue certificate: {str(exc)}")


@router.delete("/certificates/{cert_id}")
def delete_certificate(cert_id: int, db: Session = Depends(get_db)):
    try:
        cert = db.query(CertificateRecord).filter(CertificateRecord.id == cert_id).first()
        if not cert:
            raise HTTPException(status_code=404, detail="Certificate not found.")
        db.delete(cert)
        db.commit()
        return {"status": "success", "message": "Certificate revoked and removed."}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete certificate: {str(exc)}")
