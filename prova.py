import win32gui
import win32con
result = win32gui.MessageBox(0, "Would you like to see the simple version?", "MessageBox Example", win32con.MB_YESNO); 
if result == win32con.IDYES:
    win32gui.MessageBox(0, "No caption, one button.", "", win32con.MB_OK)