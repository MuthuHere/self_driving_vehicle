import cv2
import win32gui, win32ui, win32con, win32api
import numpy as np

def cap(region=None):
    hwin = win32gui.GetDesktopWindow()

    if region:
        left, top, x2, y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
    else:
        width = win32api.getSystemMetric(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.getSystemMetric(win32con.SM_CYVITUALSCREEN)
        left = win32api.getSystemMetric(win32con.SM_XVIRTUALSCREEN)
        top = win32api.getSystemMetric(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, height, width)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0,0), (width,height), srcdc, (left,top), win32con.SRCCOPY)

    signedIntsArray = bmp.getBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
