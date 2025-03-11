import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import yt_dlp

class YoutubeDownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("Youtube Video Downloader by NoeKz")
        master.geometry("550x400")
        
        # Label dan Input URL
        self.url_label = tk.Label(master, text="Masukkan URL YouTube:")
        self.url_label.pack(pady=(10, 0))
        
        self.url_entry = tk.Entry(master, width=60)
        self.url_entry.pack(pady=(0, 10))
        
        # Label dan Input folder output
        self.folder_label = tk.Label(master, text="Folder Output:")
        self.folder_label.pack()
        
        self.folder_frame = tk.Frame(master)
        self.folder_frame.pack(pady=(0, 10))
        
        self.folder_var = tk.StringVar()
        self.folder_entry = tk.Entry(self.folder_frame, textvariable=self.folder_var, width=45)
        self.folder_entry.pack(side=tk.LEFT)
        
        self.browse_button = tk.Button(self.folder_frame, text="Browse", command=self.browse_folder)
        self.browse_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Tombol download
        self.download_button = tk.Button(master, text="Download", command=self.start_download)
        self.download_button.pack(pady=(0, 10))
        
        # Area status untuk menampilkan log download
        self.status_text = tk.Text(master, height=10, width=65, state=tk.DISABLED)
        self.status_text.pack(pady=(0, 10))
        
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_var.set(folder_selected)
            
    def log_status(self, message):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        
    def download_progress_hook(self, d):
        # Callback untuk memantau progress download
        if d['status'] == 'downloading':
            percentage = d.get('_percent_str', '').strip()
            speed = d.get('_speed_str', '').strip()
            eta = d.get('_eta_str', '').strip()
            self.log_status(f"Downloading... {percentage} | Kecepatan: {speed} | ETA: {eta}")
        elif d['status'] == 'finished':
            self.log_status("Download selesai, sedang menggabungkan video dengan audio")
            
    def start_download(self):
        # Validasi input URL dan folder output
        url = self.url_entry.get().strip()
        output_folder = self.folder_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Masukkan URL YouTube!")
            return
        
        if not output_folder:
            messagebox.showerror("ERROR", "Pilih folder output!")
            return
        
        self.download_button.config(state=tk.DISABLED)
        self.log_status("Memulai download...")
        
        # Gunakan threading agar UI tidak freeze saat proses download berlangsung
        threading.Thread(target=self.download_video, args=(url, output_folder), daemon=True).start()
        
    def download_video(self, url, output_folder):
        ydl_opts = {
            # Mengunduh video dan audio terbaik, lalu menggabungkannya menggunakan FFMpeg
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
            'progress_hooks': [self.download_progress_hook],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.log_status("Download dan Merge berhasil!")
        except Exception as e:
            self.log_status(f"Terjadi error: {str(e)}")
        finally:
            self.download_button.config(state=tk.NORMAL)
            
if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloaderApp(root)
    root.mainloop()