import re
from datetime import datetime
from model.model import BaseModel
from model.normal_model import NormalApplicationModel
from model.internship_model import InternshipApplicationModel

class Controller:
    def __init__(self):
        self.model = BaseModel()

    # แสดงตำแหน่งงานที่เปิด
    def list_jobs(self):
        jobs = self.model.get_open_jobs()
        companies = self.model.db["companies"]
        return jobs, companies

    # ตรวจสอบอีเมล
    def validate_email(self, email) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    # สมัครงาน
    def apply_job(self, job_id):
        job = self.model.get_job(job_id)
        cand = self.current_user

        if not job:
            return False, "ไม่พบตำแหน่งงาน"
        if not cand:
            return False, "ไม่พบผู้สมัคร"
        if job["status"] != "open":
            return False, "ตำแหน่งนี้ปิดรับสมัครแล้ว"
        if job["deadline"] < datetime.now().strftime("%Y-%m-%d"):
            return False, "หมดเขตรับสมัครแล้ว"

        # เลือกโมเดลตาม job_type
        if job["job_type"] == "normal":
            model = NormalApplicationModel()
            return model.apply(job_id, cand["id"])
        elif job["job_type"] == "internship":
            model = InternshipApplicationModel()
            return model.apply(job_id, cand["id"])
        else:
            return False, "ประเภทงานไม่ถูกต้อง"

    
    # สำหรับยืนยันตัวตน
    def authenticate(self, cand_id, email):
        cand = self.model.get_candidate(cand_id)
        if cand and cand["email"] == email and self.validate_email(email):
            self.current_user = cand
            return True, f"ยินดีต้อนรับ {cand['first_name']} {cand['last_name']}"
        return False, ">>> รหัสผู้สมัครหรืออีเมลไม่ถูกต้อง"
