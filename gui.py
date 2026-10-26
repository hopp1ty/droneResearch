import tkinter as tk
import subprocess as sub
import os, signal
root = tk.Tk()

#global variables
window = None
camera = None

#gui setup
label = tk.Label(root, text="Drone GUI")
label.pack()
root.geometry("400x200")
root.configure(bg='darkgray')


def command_drone():
    global window
    global camera
    if window is not None and window.poll() is None:
        return
    window = sub.Popen(["cmd.exe", "/k", "wsl", "cd ~/droneResearch" ]
    , start_new_session=True )
    #&& python3 fly.py", 
    #creationflags=subprocess.CREATE_NO_WINDOW
    if camera is not None and camera.poll() is None:
       return
    camera = sub.Popen(["cmd.exe", "/k", "wsl", "cd ~/droneResearch" ]
    , start_new_session=True )
    #&&px4 camera
    
def stop_drone():
    global window
    global camera
    if window is not None and window.poll() is None:
        os.killpg(os.getpgid(window.pid), signal.SIGTERM)
        window.wait()
    window = None
    if camera is not None and window.poll() is None:
        os.killpg(os.getpgid(camera.pid), signal.SIGTERM)
        camera.wait()
    camera = None
#button for gui
start = tk.Button(root, text="Start", bg="lightgray", command= command_drone)
stop = tk.Button(root, text="Stop", bg="lightgray", command = stop_drone)

#put button inside at coordinates
start.pack(padx = 20, pady = 20)
stop.pack(padx=20, pady=0)

#runs window, keeps responsive
root.mainloop() 