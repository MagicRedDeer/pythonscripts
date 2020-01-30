from os import path
from ctypes import *
from ctypes.wintypes import *

# Python implementation of:
#
# typedef struct {
#       DWORD   ReparseTag;
#       DWORD   ReparseDataLength;
#       WORD    Reserved;
#       WORD    ReparseTargetLength;
#       WORD    ReparseTargetMaximumLength;
#       WORD    Reserved1;
#       WCHAR   ReparseTarget[1];
# } REPARSE_MOUNTPOINT_DATA_BUFFER, *PREPARSE_MOUNTPOINT_DATA_BUFFER;

MAX_PATH = 260

class ReparsePoint(Structure):
    _fields_ = [
        ("ReparseTag", DWORD),
        ("ReparseDataLength", DWORD),
        ("Reserved", WORD),

        ("ReparseTargetLength", WORD),
        ("ReparseTargetMaximumLength", WORD),
        ("Reserved1", WORD),
        ("ReparseTarget", c_wchar * MAX_PATH),
    ]

GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000

FILE_SHARE_DELETE = 0x00000004
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
FILE_SHARE_READ_WRITE = (FILE_SHARE_READ | FILE_SHARE_WRITE)

OPEN_EXISTING = 3

IO_REPARSE_TAG_MOUNT_POINT = 0xA0000003
REPARSE_MOUNTPOINT_HEADER_SIZE = 8

FSCTL_SET_REPARSE_POINT = 589988
FILE_FLAG_OPEN_REPARSE_POINT = 2097152
FILE_FLAG_BACKUP_SEMANTICS = 33554432
FILE_FLAG_REPARSE_BACKUP = 35651584 # FILE_FLAG_OPEN_REPARSE_POINT | FILE_FLAG_BACKUP_SEMANTICS

INVALID_HANDLE_VALUE = -1
LPOVERLAPPED = c_void_p
LPSECURITY_ATTRIBUTES = c_void_p

NULL = 0
FALSE = BOOL(0)
TRUE = BOOL(1)

def CreateFile(filename, access, sharemode, creation, flags):
    return HANDLE(windll.kernel32.CreateFileW(
        LPWSTR(filename),
        DWORD(access),
        DWORD(sharemode),
        LPSECURITY_ATTRIBUTES(NULL),
        DWORD(creation),
        DWORD(flags),
        HANDLE(NULL)
    ))

def CreateDirectory(fpath):
    return windll.kernel32.CreateDirectoryW(LPWSTR(fpath), LPSECURITY_ATTRIBUTES(NULL)) != FALSE

def RemoveDirectory(fpath):
    return windll.kernel32.RemoveDirectoryW(LPWSTR(fpath)) != FALSE

def translate_path(fpath):
    fpath = path.abspath(fpath)
    if fpath[len(fpath)-1] == '\\' and fpath[len(fpath)-2] == ':':
        fpath = fpath[:len(fpath)-1]
    return '\\??\\%s' % fpath

def junction(source, link_name):
    """ Create a junction at link_name pointing to source directory. """
    if not path.isdir(source):
        raise Exception('Junction source does not exist or is not a directory.')

    link_name = path.abspath(link_name)
    if path.exists(link_name):
        raise Exception('Filepath for new junction already exists.')

    if not CreateDirectory(link_name):
        raise Exception('Failed to create new directory for target junction.')

    source = translate_path(source)
    hFile = CreateFile(link_name, GENERIC_WRITE, 0, OPEN_EXISTING, FILE_FLAG_REPARSE_BACKUP)
    if hFile == HANDLE(INVALID_HANDLE_VALUE):
        raise Exception('Failed to open directory for junction creation.')

    datalen = len(source) * sizeof(c_wchar)
    reparseInfo = ReparsePoint(
        IO_REPARSE_TAG_MOUNT_POINT,
        datalen + 12,
        0,
        datalen,
        datalen + sizeof(c_wchar),
        0,
        source
    )
    pReparseInfo = pointer(reparseInfo)

    print reparseInfo.ReparseTarget
    returnedLength = DWORD(0)
    reparseInfo._fields_[6] = ('ReparseTarget', datalen)
    result = BOOL(
        windll.kernel32.DeviceIoControl(
            hFile,
            DWORD(FSCTL_SET_REPARSE_POINT),
            pReparseInfo,
            DWORD(reparseInfo.ReparseDataLength + REPARSE_MOUNTPOINT_HEADER_SIZE),
            LPVOID(NULL),
            DWORD(0),
            byref(returnedLength),
            LPOVERLAPPED(NULL)
        )
    ) == TRUE

    #if not result:
        #RemoveDirectory(link_name)

    windll.kernel32.CloseHandle(hFile)
    return result

print junction(r'\\dbserver\assets\dettol_3', 'test')
"""
Just putting this here for the moment so I know how to call the function.   

BOOL WINAPI DeviceIoControl(
  __in         HANDLE hDevice,
  __in         DWORD dwIoControlCode,
  __in_opt     LPVOID lpInBuffer,
  __in         DWORD nInBufferSize,
  __out_opt    LPVOID lpOutBuffer,
  __in         DWORD nOutBufferSize,
  __out_opt    LPDWORD lpBytesReturned,
  __inout_opt  LPOVERLAPPED lpOverlapped
);
"""
