ASM_FILE_BEGIN = """format PE console\nentry start
include 'INCLUDE\\win32a.inc'
section '.data' data readable writeable\n"""
                
ASM_FILE_AFTER_BEGIN = "section '.code' code readable writeable executable\n\tstart:\n"
                        
ASM_FILE_END = """\t\tinvoke ExitProcess, 0
section '.idata' data import readable
\tlibrary kernel, 'kernel32.dll', msvcrt, 'msvcrt.dll'
\timport kernel, ExitProcess, 'ExitProcess'
\timport msvcrt, printf, 'printf'\n"""
                