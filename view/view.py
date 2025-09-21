class View:
    def show_menu(ctrl):
        while True:
            print("\n==== ระบบรับสมัครงาน (Job Fair) ====")
            print("1. ดูตำแหน่งงานที่เปิด")
            print("2. สมัครงาน")
            print("0. ออก")

            choice = input("เลือกเมนู: ")
            if choice == "1":
                jobs, companies = ctrl.list_jobs()
                View.show_jobs(jobs, companies)
            elif choice == "2":
                print("\n=== สมัครงาน ===")
                print("พิมพ์ 0 เพื่อลกลับไปที่เมนูก่อนหน้า")
                job_id = input("กรอกรหัสงาน: ").strip()
                if job_id == "0":
                    continue

                success, msg = ctrl.apply_job(job_id)   # ✅ ส่งแค่ job_id
                View.show_message(msg)
            elif choice == "0":
                break
            else:
                print("ตัวเลือกไม่ถูกต้อง")

    def show_jobs(jobs, companies):
        print("\n=== ตำแหน่งงานที่เปิดรับ ===")
        if not jobs:
            print("ไม่มีงานที่เปิดรับสมัครในตอนนี้")
            return
        for j in jobs:
            comp = next((c for c in companies if c["id"] == j["company_id"]), None)
            comp_name = comp["name"] if comp else "Unknown"
            print(f"[{j['id']}] {j['title']} - {comp_name}")
            print(f"   ประเภท: {j['job_type']} | ปิดรับ: {j['deadline']} | สถานะ: {j['status']}")
            print(f"   รายละเอียด: {j['desc']}")

    def show_message(msg):
        print(f"\n>>> {msg}")

    def login(ctrl):
        print("\n=== Login ===")
        while True:
            cand_id = input("กรอกรหัสผู้สมัคร: ").strip()
            email = input("กรอกอีเมล: ").strip()

            success, msg = ctrl.authenticate(cand_id, email)
            print(msg)
            if success:
                break
