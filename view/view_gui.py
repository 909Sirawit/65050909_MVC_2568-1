import tkinter as tk
from tkinter import messagebox
from controller.controller import Controller

class JobApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ระบบรับสมัครงาน (Job Fair Q2)")
        self.root.geometry("800x600")

        # ตั้งค่า grid หลักให้ยืดเต็มหน้าจอ
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.ctrl = Controller()
        self.show_login_screen()

    def center_window(self, window, width=400, height=200):
        window.update_idletasks()  # อัปเดตค่าหน้าต่างก่อน
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")


    def show_login_screen(self):
        self.clear_screen()

        frame = tk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")

        # จัด row/col ให้ frame กึ่งกลาง
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(5, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        tk.Label(frame, text="เข้าสู่ระบบผู้สมัคร", font=("Arial", 16)).grid(row=1, column=1, pady=10)

        tk.Label(frame, text="อีเมล:").grid(row=2, column=0, sticky="e", padx=5)
        self.entry_email = tk.Entry(frame, width=30)
        self.entry_email.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="รหัสผู้สมัคร:").grid(row=3, column=0, sticky="e", padx=5)
        self.entry_cand_id = tk.Entry(frame, width=30)
        self.entry_cand_id.grid(row=3, column=1, pady=5)

        tk.Button(frame, text="เข้าสู่ระบบ", command=self.login).grid(row=4, column=1, pady=15)

    def login(self):
        cand_id = self.entry_cand_id.get().strip()
        email = self.entry_email.get().strip()
        success, msg = self.ctrl.authenticate(cand_id, email)
        messagebox.showinfo("ผลการเข้าสู่ระบบ", msg)
        if success:
            self.show_main_menu()

    def show_main_menu(self):
        self.clear_screen()

        frame = tk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(5, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        tk.Label(frame, text="เมนูหลัก", font=("Arial", 16)).grid(row=1, column=1, pady=10)

        tk.Button(frame, text="ดูตำแหน่งงาน", width=20, command=self.show_jobs).grid(row=2, column=1, pady=5)
        tk.Button(frame, text="สมัครงาน", width=20, command=self.apply_job_popup).grid(row=3, column=1, pady=5)
        tk.Button(frame, text="ออก", width=20, command=self.root.quit).grid(row=4, column=1, pady=5)

    def show_jobs(self):
        jobs, companies = self.ctrl.list_jobs()
        popup = tk.Toplevel(self.root)
        popup.title("ตำแหน่งงานที่เปิดรับ")
        self.center_window(popup, 600, 400)

        if not jobs:
            tk.Label(popup, text="ไม่มีงานที่เปิดรับสมัครในตอนนี้").pack(pady=20)
            return

        text = tk.Text(popup, wrap="word")
        text.pack(expand=True, fill="both", padx=10, pady=10)

        for j in jobs:
            comp = next((c for c in companies if c["id"] == j["company_id"]), None)
            comp_name = comp["name"] if comp else "Unknown"
            text.insert("end", f"[{j['id']}] {j['title']} - {comp_name}\n"
                            f"ประเภท: {j['job_type']} | ปิดรับ: {j['deadline']}\n"
                            f"รายละเอียด: {j['desc']}\n\n")

        text.config(state="disabled")


    def apply_job_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("สมัครงาน")
        self.center_window(popup, 400, 200)

        tk.Label(popup, text="กรอกรหัสงาน:").pack(pady=5)
        entry_job = tk.Entry(popup)
        entry_job.pack(pady=5)
        tk.Button(popup, text="สมัคร", command=lambda: self.apply_job(entry_job.get(), popup)).pack(pady=10)

    def apply_job(self, job_id, popup):
        success, msg = self.ctrl.apply_job(job_id)
        messagebox.showinfo("ผลการสมัคร", msg)
        popup.destroy()
        self.show_main_menu()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = JobApp(root)
    root.mainloop()
