from model.model import BaseModel
from datetime import datetime

class NormalApplicationModel(BaseModel):
    """สมัครงานปกติ (รับเฉพาะผู้ที่จบแล้ว)"""
    def apply(self, job_id, cand_id):
        job = self.get_job(job_id)
        cand = self.get_candidate(cand_id)

        if not job:
            return False, "ไม่พบตำแหน่งงาน"
        if not cand:
            return False, "ไม่พบผู้สมัคร"
        if job["job_type"] != "normal":
            return False, "ตำแหน่งนี้ไม่ใช่งานปกติ"
        if cand["status"] != "graduated":
            return False, "งานปกติรับเฉพาะผู้ที่จบแล้ว"
        if job["deadline"] < datetime.now().strftime("%Y-%m-%d"):
            return False, "หมดเขตรับสมัครแล้ว"

        self.db["applications"].append({
            "job_id": job_id,
            "candidate_id": cand_id,
            "applied_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save()
        return True, "สมัครงานปกติสำเร็จ"