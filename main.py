import tkinter as tk
from tkinter import filedialog, scrolledtext
import subprocess
import threading

class RobocopyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Robocopy 工具")
        self.root.geometry("600x500")

        # --- UI 組件 ---
        # 來源路徑
        tk.Label(root, text="來源路徑 (Source):").pack(pady=5)
        self.src_entry = tk.Entry(root, width=60)
        self.src_entry.pack(padx=10)
        tk.Button(root, text="瀏覽...", command=self.browse_src).pack()

        # 目標路徑
        tk.Label(root, text="目標路徑 (Destination):").pack(pady=5)
        self.dst_entry = tk.Entry(root, width=60)
        self.dst_entry.pack(padx=10)
        tk.Button(root, text="瀏覽...", command=self.browse_dst).pack()

        # 參數選項 (Checkboxes)
        self.mir_var = tk.BooleanVar()
        tk.Checkbutton(root, text="鏡像模式 (/MIR) - 會刪除目標多餘檔案", variable=self.mir_var).pack()
        
        self.z_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="斷點續傳模式 (/Z)", variable=self.z_var).pack()

        # 執行按鈕
        tk.Button(root, text="開始執行", bg="green", fg="white", command=self.start_thread).pack(pady=10)

        # 日誌輸出區
        self.log_area = scrolledtext.ScrolledText(root, height=15)
        self.log_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def browse_src(self):
        path = filedialog.askdirectory()
        self.src_entry.delete(0, tk.END)
        self.src_entry.insert(0, path)

    def browse_dst(self):
        path = filedialog.askdirectory()
        self.dst_entry.delete(0, tk.END)
        self.dst_entry.insert(0, path)

    def start_thread(self):
        # 使用線程避免 GUI 凍結
        thread = threading.Thread(target=self.run_robocopy)
        thread.start()

    def run_robocopy(self):
        src = self.src_entry.get()
        dst = self.dst_entry.get()
        
        # 組合指令
        cmd = ["robocopy", src, dst, "/E"]
        if self.mir_var.get(): cmd.append("/MIR")
        if self.z_var.get(): cmd.append("/Z")
        
        self.log_area.insert(tk.END, f"執行指令: {' '.join(cmd)}\n\n")
        
        # 執行並即時讀取輸出
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
        
        for line in process.stdout:
            self.log_area.insert(tk.END, line)
            self.log_area.see(tk.END) # 自動滾動到底部
        
        process.wait()
        self.log_area.insert(tk.END, "\n--- 任務完成 ---")

if __name__ == "__main__":
    root = tk.Tk()
    app = RobocopyGUI(root)
    root.mainloop()