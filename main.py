import cv2
from threading import Thread
from os.path import join
from sys import stdout
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

if __name__ == "__main__":
    def saveImg(frame, idx, path):
        cv2.imwrite(join(path, "img_{}.png".format(idx)), frame)


    def extractAndSave(vid_path, img_path):
        info.config(text="", fg="#000000")
        root.update()
        if vid_path == "" or img_path == "":
            info.config(text="Please input a path.", fg="#ff0000")
            root.update()
            return
        threads = []
        cap = cv2.VideoCapture(vid_path)

        idx = 0

        while 1:
            ret, frame = cap.read()
            if not ret:
                cap.release()
                break
            t = Thread(target=saveImg, args=(frame, idx, img_path))
            threads.append(t)
            t.start()
            idx += 1
            info.config(text="extracting pictures {}".format(idx), fg="#000000")
            root.update()

        for idx, t in enumerate(threads):
            info.config(text="finishing {}/{}".format(idx + 1, len(threads)), fg="#000000")
            root.update()
            t.join()


    def open_vid_path():
        vid_path_entry.delete(0)
        vid_path_entry.insert(0, filedialog.askopenfilename(initialdir="\\", title="select a file",
                                                            filetypes=(("all files", "*.*"))))


    def open_img_path():
        img_path_entry.delete(0)
        img_path_entry.insert(0, filedialog.askdirectory())


    root = tk.Tk()
    f1 = tk.Frame(root)
    f1.pack(padx=10, pady=10)

    tk.Label(f1, text="Video").grid(column=0, row=0, sticky=tk.NW)
    vid_path_entry = ttk.Entry(f1, width=50)
    vid_path_entry.grid(column=1, row=0)
    ttk.Button(f1, text="Open", command=open_vid_path).grid(column=2, row=0)

    tk.Label(f1, text="Img Folder").grid(column=0, row=1, sticky=tk.NW)
    img_path_entry = ttk.Entry(f1, width=50)
    img_path_entry.grid(column=1, row=1)
    ttk.Button(f1, text="Open", command=open_img_path).grid(column=2, row=1)

    info = tk.Label(f1, text="")
    info.grid(column=1, row=2)

    ttk.Button(f1, text="Start", command=lambda: extractAndSave(vid_path_entry.get(), img_path_entry.get())).grid(
        column=2, row=3, sticky=tk.NE)

    root.mainloop()
