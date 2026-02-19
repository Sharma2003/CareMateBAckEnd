from uuid import uuid4, UUID
from redis import Redis
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database.core import SessionLocal
from entities.ReportMaster import ReportMaster
from entities.PatientReport import PatientReport
from entities.DoctorReport import DoctorReport
from chat.src.graph.nodes import update_report
from chat.src.graph.state import InterviewReport
import asyncio

load_dotenv()
redis = Redis(
    host="localhost",    
    port=6380,
    db=0,
    decode_responses=False
)


def generate_reports_job(patient_id, doctor_id, state:dict):
    db: Session = SessionLocal()

    try:
        # report_state = InterviewReport(**state)
        report_state = InterviewReport(**state)
        updated_state = asyncio.run(update_report(state=report_state))
        master = ReportMaster(
            patient_id=patient_id,
            doctor_id=doctor_id,
            job_status='completed'
        )
        db.add(master)
        db.flush()

        db.add(PatientReport(
            master_id = master.id,
            report_md=updated_state.patient_report_md
        ))

        db.add(DoctorReport(
            master_id = master.id,
            report_md=updated_state.doctor_report_md
        ))

        db.commit()
        db.refresh(master)


    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
