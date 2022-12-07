format PE console
entry start
include 'INCLUDE\win32a.inc'
section '.data' data readable writeable
	format_int db '%d', 0
	format_str db '%s', 0
	s_0 db  "Happy!!!", 0
section '.code' code readable writeable executable
	start:
		push 10
addr_2:
		pop eax
		push eax
		push eax
		push 0
		mov ecx, 0
		mov edx, 1
		pop ebx
		pop eax
		cmp eax, ebx
		cmovge ecx, edx
		push ecx
		pop eax
		test eax, eax
		jz addr_1
		pop eax
		push eax
		push eax
		pop eax
		cinvoke printf, format_int, eax
		xor eax, eax
		pop eax
		push eax
		push eax
		push 5
		mov ecx, 0
		mov edx, 1
		pop ebx
		pop eax
		cmp eax, ebx
		cmove ecx, edx
		push ecx
		pop eax
		test eax, eax
		jz addr_0
		push s_0
		pop eax
		cinvoke printf, format_str, eax
		xor eax, eax
addr_0:
		push 1
		pop ebx
		pop eax
		sub eax, ebx
		push eax
		jmp addr_2
addr_1:
		invoke ExitProcess, 0
section '.idata' data import readable
	library kernel, 'kernel32.dll', msvcrt, 'msvcrt.dll'
	import kernel, ExitProcess, 'ExitProcess'
	import msvcrt, printf, 'printf'
