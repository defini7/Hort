ASM_FILE_BEGIN = "format PE console\n \
                entry start\n \
                include 'INCLUDE\\win32a.inc'\n \
                section '.data' data readable writeable\n"
                
ASM_FILE_AFTER_BEGIN = "section '.code' code readable writeable executable\n \
                        \tstart:\n"
                        
ASM_FILE_END = "\t\tinvoke ExitProcess, 0\n \
                section '.idata' data import readable\n \
                \tlibrary kernel, 'kernel32.dll', msvcrt, 'msvcrt.dll'\n \
                \timport kernel, ExitProcess, 'ExitProcess'\n \
                \timport msvcrt, printf, 'printf'\n"
                