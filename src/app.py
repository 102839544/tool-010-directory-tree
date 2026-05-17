#!/usr/bin/env python3
"""
目录树生成工具 - 生成文件夹结构树
"""
import sys, os, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext

class App:
    def __init__(self, root):
        self.root = root
        root.title("目录树生成工具 v1.0")
        root.geometry("700x600")
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#00796b", height=50)
        f.pack(fill="x")
        tk.Label(f, text="🌳 目录树生成工具", font=("Arial",14,"bold"),
                 fg="white", bg="#00796b").pack(pady=12)
        
        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill="both", expand=True)
        
        bf = tk.Frame(main)
        bf.pack(fill="x", pady=5)
        tk.Button(bf, text="选择文件夹", command=self.select_folder,
                  bg="#00796b", fg="white", padx=15).pack(side="left", padx=5)
        tk.Button(bf, text="生成目录树", command=self.generate,
                  bg="#4caf50", fg="white", padx=15).pack(side="left", padx=5)
        tk.Button(bf, text="复制结果", command=self.copy_result,
                  padx=15).pack(side="left", padx=5)
        tk.Button(bf, text="保存为文件", command=self.save,
                  bg="#ff9800", fg="white", padx=15).pack(side="left", padx=5)
        
        # 选项
        of = tk.Frame(main)
        of.pack(fill="x", pady=5)
        self.show_files = tk.BooleanVar(value=True)
        self.max_depth = tk.StringVar(value="3")
        tk.Checkbutton(of, text="显示文件", variable=self.show_files).pack(side="left", padx=10)
        tk.Label(of, text="最大深度：").pack(side="left", padx=(20,5))
        tk.Entry(of, textvariable=self.max_depth, width=5).pack(side="left")
        
        # 结果
        self.result_txt = scrolledtext.ScrolledText(main, font=("Consolas",10), height=25)
        self.result_txt.pack(fill="both", expand=True, pady=10)
        
        self.status = tk.Label(main, text="选择文件夹生成目录树",
                               font=("Arial",10), fg="gray")
        self.status.pack()
    
    def select_folder(self):
        self.folder = filedialog.askdirectory(title="选择文件夹")
        if self.folder:
            self.status.config(text=f"已选择：{Path(self.folder).name}")
    
    def generate_tree(self, path, prefix="", depth=0, max_depth=3):
        """递归生成目录树"""
        result = []
        path = Path(path)
        
        if depth > max_depth:
            return result
        
        items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        
        # 过滤隐藏文件和常见忽略目录
        ignore_dirs = {".git", "__pycache__", "node_modules", ".idea", ".vscode", "venv", "env"}
        items = [i for i in items if not i.name.startswith(".") and i.name not in ignore_dirs]
        
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            
            if item.is_dir():
                connector = "└── " if is_last else "├── "
                result.append(prefix + connector + f"📁 {item.name}/")
                
                if depth < max_depth:
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    result.extend(self.generate_tree(item, new_prefix, depth + 1, max_depth))
            
            elif self.show_files.get():
                connector = "└── " if is_last else "├── "
                result.append(prefix + connector + f"📄 {item.name}")
        
        return result
    
    def generate(self):
        if not hasattr(self, "folder"):
            messagebox.showwarning("提示", "请先选择文件夹")
            return
        
        try:
            max_depth = int(self.max_depth.get())
        except:
            max_depth = 3
        
        folder_name = Path(self.folder).name
        tree_lines = [f"📁 {folder_name}/"]
        
        tree_lines.extend(self.generate_tree(self.folder, max_depth=max_depth))
        
        self.result_txt.delete(1.0, "end")
        self.result_txt.insert(1.0, "\n".join(tree_lines))
        
        self.status.config(text=f"✅ 生成完成（{len(tree_lines)} 项）")
    
    def copy_result(self):
        text = self.result_txt.get(1.0, "end")
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("复制成功", "目录树已复制到剪贴板")
    
    def save(self):
        text = self.result_txt.get(1.0, "end")
        if not text.strip():
            messagebox.showwarning("提示", "请先生成目录树")
            return
        
        f = filedialog.asksaveasfilename(title="保存",
             defaultextension=".txt", filetypes=[("文本","*.txt"),("Markdown","*.md")])
        if f:
            with open(f, "w", encoding="utf-8") as file:
                file.write(text)
            messagebox.showinfo("保存成功", f"已保存至：{f}")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
