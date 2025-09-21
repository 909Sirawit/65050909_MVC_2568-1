import json

DB_FILE = "sample_data.json"

class BaseModel:
    def __init__(self):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                self.db = json.load(f)
        except FileNotFoundError:
            self.db = {"companies": [], "jobs": [], "candidates": [], "applications": []}
            self.save()

    def save(self):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(self.db, f, indent=4, ensure_ascii=False)

    def save_table(self, table=None):
        """บันทึกฐานข้อมูล (ทั้งก้อน เพราะใช้ JSON ไฟล์เดียว)"""
        self.save()

    def get_open_jobs(self, job_type=None):
        jobs = [job for job in self.db["jobs"] if job["status"] == "open"]
        if job_type:
            jobs = [j for j in jobs if j["job_type"] == job_type]
        return jobs

    def get_candidate(self, cand_id):
        return next((c for c in self.db["candidates"] if c["id"] == cand_id), None)

    def get_job(self, job_id):
        return next((j for j in self.db["jobs"] if j["id"] == job_id), None)
