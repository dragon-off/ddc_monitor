from ctypes import windll, byref, Structure, WinError, POINTER, WINFUNCTYPE
from ctypes.wintypes import BOOL, HMONITOR, HDC, RECT, LPARAM, DWORD, BYTE, WCHAR, HANDLE

_MONITORENUMPROC = WINFUNCTYPE(BOOL, HMONITOR, HDC, POINTER(RECT), LPARAM)

class _PHYSICAL_MONITOR(Structure):
    _fields_ = [('handle', HANDLE),
                ('description', WCHAR * 128)]

def _iter_physical_monitors(close_handles=True):
    def callback(hmonitor, hdc, lprect, lparam):
        monitors.append(HMONITOR(hmonitor))
        return True

    monitors = []
    if not windll.user32.EnumDisplayMonitors(None, None, _MONITORENUMPROC(callback), None):
        raise WinError('EnumDisplayMonitors failed')

    for monitor in monitors:
        # get physical monitor count
        count = DWORD()
        if not windll.dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(monitor, byref(count)):
            raise WinError()
        # get physical monitor handles
        physical_array = (_PHYSICAL_MONITOR * count.value)()
        if not windll.dxva2.GetPhysicalMonitorsFromHMONITOR(monitor, count.value, physical_array):
            raise WinError()
        for physical in physical_array:
            yield physical.handle
            if close_handles:
                if not windll.dxva2.DestroyPhysicalMonitor(physical.handle):
                    raise WinError()


def set_vcp_feature(monitor, code, value):
    if not windll.dxva2.SetVCPFeature(HANDLE(monitor), BYTE(code), DWORD(value)):
        raise WinError()

for handle in _iter_physical_monitors():
	# on- 0x01; off- 0x04
	#Restore Factory Defaults 0x04 set >0
	#Restore Factory Luminance/ Contrast Defaults 0x05 set >0
	#Restore Factory Color Defaults 0x08 set >0
	#Luminance 0x10 set 0-100
	#Contrast 0x12 set 0-100
	#Power Mode 0xD6 set 0x01-on,0x05-off
	#Input Source 0x60 set 0x01-D-sub; 0x03-DVI; 0x11-HDMI
	#Audio: Speaker Volume 0x62 set >0
	#Audio Mute 0x8D set 0x01-on, 0x02-off
    set_vcp_feature(handle, 0xd6, 0x04) 
   
