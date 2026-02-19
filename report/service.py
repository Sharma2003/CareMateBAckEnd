from entities.ReportMaster import ReportMaster
from entities.DoctorReport import DoctorReport
from entities.PatientReport import PatientReport


from sqlalchemy.orm import Session
from uuid import UUID


def get_patient_report(db:Session, patient_id : UUID):
    patient_report = db.query(ReportMaster.doctor_id, PatientReport.report_md).join(ReportMaster, PatientReport.master_id == ReportMaster.id).filter(ReportMaster.patient_id == patient_id).order_by(ReportMaster.created_at.desc()).all()
    return {row[0]:row[1] for row in patient_report}

# def get_doctor_report(db:Session, patient_id : UUID):
#     patient_report = db.query(PatientReport.report_md).join(ReportMaster, PatientReport.master_id == ReportMaster.id).filter(ReportMaster.patient_id == patient_id).order_by(ReportMaster.created_at.desc()).all()
#     return patient_report

def get_doctor_report(db:Session, doctor_id:UUID):
    doctor_report = db.query(DoctorReport.report_md, ReportMaster.patient_id).join(ReportMaster, DoctorReport.master_id == ReportMaster.id).filter(ReportMaster.doctor_id == doctor_id).order_by(ReportMaster.created_at.desc()).all()
    return [row[0] for row in doctor_report]
