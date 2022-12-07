def push(value):
    return f"\t\tpush {value}\n"

def plus():
    return """\t\tpop ebx
\t\tpop eax
\t\tadd eax, ebx
\t\tpush eax\n"""
            
def minus():
    return """\t\tpop ebx
\t\tpop eax
\t\tsub eax, ebx
\t\tpush eax\n"""
            
def inc():
    return """\t\tpop eax
\t\tinc eax
\t\tpush eax\n"""
            
def dec():
    return """\t\tpop eax
\t\tdec eax
\t\tpush eax\n"""
            
def bit_shl():
    return """\t\tpop eax
\t\tshl eax
\t\tpush eax\n"""
            
def bit_shr():
    return """\t\tpop eax
\t\tshl eax
\t\tpush eax\n"""
            
def bit_xor():
    return """\t\tpop ebx
\t\tpop eax
\t\txor eax, ebx
\t\tpush eax\n"""
            
def bit_or():
    return """\t\tpop ebx
\t\tpop eax
\t\tor eax, ebx
\t\tpush eax\n"""
            
def bit_and():
    return """\t\tpop ebx
\t\tpop eax
\t\tand eax, ebx
\t\tpush eax\n"""
            
def bit_not():
    return """\t\tpop ebx
\t\tpop eax
\t\tnot eax, ebx
\t\tpush eax\n"""
            
def equ():
    return """\t\tmov ecx, 0
\t\tmov edx, 1
\t\tpop ebx
\t\tpop eax
\t\tcmp eax, ebx
\t\tcmove ecx, edx
\t\tpush ecx\n"""
            
def nequ():
    return """\t\tmov ecx, 0
\t\tmov edx, 1
\t\tpop ebx
\t\tpop eax
\t\tcmp eax, ebx
\t\tcmovne ecx, edx
\t\tpush ecx\n"""
            
def greater():
    return """\t\tmov ecx, 0
\t\tmov edx, 1
\t\tpop ebx
\t\tpop eax
\t\tcmp eax, ebx
\t\tcmovg ecx, edx
\t\tpush ecx\n"""
            
def less():
    return """\t\tmov ecx, 0
\t\tmov edx, 1
\t\tpop ebx
\t\tpop eax
\t\tcmp eax, ebx
\t\tcmovl ecx, edx
\t\tpush ecx\n"""
            
def gequ():
    return """\t\tmov ecx, 0
\t\tmov edx, 1
\t\tpop ebx
\t\tpop eax
\t\tcmp eax, ebx
\t\tcmovge ecx, edx
\t\tpush ecx\n"""
            
def lequ():
    return """\t\tmov ecx, 0
\t\tmov edx, 1
\t\tpop ebx
\t\tpop eax
\t\tcmp eax, ebx
\t\tcmovle ecx, edx
\t\tpush ecx\n"""
            
def iff(addr):
    return f"""\t\tpop eax
\t\ttest eax, eax
\t\tjz addr_{addr}\n"""
             
def elsee(after_if_addr, after_else_addr):
    return f"""\t\tjmp addr_{after_if_addr}
addr_{after_else_addr}:\n"""
            
def whilee(addr):
    return f"addr_{addr}:\n"
            
def do(addr):
    return f"""\t\tpop eax
\t\ttest eax, eax
\t\tjz addr_{addr}\n"""
            
def end_while(addr):
    return f"\t\tjmp addr_{addr}\n"

def end_if_while(addr):
    return f"addr_{addr}:\n"
    
def printt(format_method):
    return f"""\t\tpop eax
\t\tcinvoke printf, {format_method}, eax
\t\txor eax, eax\n"""
            
def clear_asm_stack(asm_stack_size, local_stack_size):
    out = ''
    for _ in range(asm_stack_size + local_stack_size):
        out += "\t\tpop eax\n"
        
    if asm_stack_size > 0:
        out += "\t\txor eax, eax\n"
        
    return out

def copy():
    return """\t\tpop eax
\t\tpush eax
\t\tpush eax\n"""
            
def pop():
    return "\t\tpop eax\n"
        