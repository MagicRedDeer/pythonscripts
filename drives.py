from ctypes import cdll, create_unicode_buffer
from ctypes.wintypes import LPCWSTR, LPWSTR, POINTER, DWORD

_get_connection = cdll.mpr.WNetGetConnectionW
_get_connection.argtypes = [
        LPCWSTR, #local_name
        LPWSTR, #remote_name
        POINTER(DWORD) #buf_len
        ]
_get_connection.restype = DWORD

def get_connection(drive):
    length = 256
    remote = create_unicode_buffer(u"\000" * length)
    res = _get_connection(drive, remote, DWORD(length))
    if not res:
        return remote.value

if __name__ == "__main__":
    drive = 'P:'
    print drive, 'is mapped to', get_connection(drive)
