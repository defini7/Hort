def push(value):
    return f"\t\tpush {value}\n"

def plus():
    return "\t\tpop ebx\n \
            \t\tpop eax\n \
            \t\tadd eax, ebx\n \
            \t\tpush eax\n"
            
def minus():
    return "\t\tpop ebx\n \
            \t\tpop eax\n \
            \t\tsub eax, ebx\n \
            \t\tpush eax\n"
            
def inc():
    return "\t\tpop eax\n \
            \t\tinc eax\n \
            \t\tpush eax\n"
            
def dec():
    return "\t\tpop eax\n \
            \t\tdec eax\n \
            \t\tpush eax\n"
            
def bit_shl():
    return "\t\tpop eax\n \
            \t\tshl eax\n \
            \t\tpush eax\n"
            
def bit_shr():
    return "\t\tpop eax\n \
            \t\tshl eax\n \
            \t\tpush eax\n"
            
def bit_xor():
    return "\t\tpop ebx\n \
            \t\tpop eax\n \
            \t\txor eax, ebx\n \
            \t\tpush eax\n"
            
def bit_or():
    return "\t\tpop ebx\n \
            \t\tpop eax\n \
            \t\tor eax, ebx\n \
            \t\tpush eax\n"
            
def bit_and():
    return "\t\tpop ebx\n \
            \t\tpop eax\n \
            \t\tand eax, ebx\n \
            \t\tpush eax\n"
            
def bit_not():
    return "\t\tpop ebx\n \
            \t\tpop eax\n \
            \t\tnot eax, ebx\n \
            \t\tpush eax\n"
            
def equ():
    return "\t\tmov ecx, 0\n \
            \t\tmov edx, 1\n \
            \t\tpop ebx\n \
            \t\tpop eax\n \
            \t\tcmp eax, ebx\n \
            \t\tcmove ecx, edx\n \
            \t\tpush ecx\n"
            
def nequ():
    return "\t\tmov ecx, 0\n \
            \t\tmov edx, 1\n \
            \t\tpop ebx\n \
            \t\tpop eax\n \
            \t\tcmp eax, ebx\n \
            \t\tcmovne ecx, edx\n \
            \t\tpush ecx\n"
            
def greater():
    return "\t\tmov ecx, 0\n \
            \t\tmov edx, 1\n \
            \t\tpop ebx\n \
            \t\tpop eax\n \
            \t\tcmp eax, ebx\n \
            \t\tcmovg ecx, edx\n \
            \t\tpush ecx\n"
            
def less():
    return "\t\tmov ecx, 0\n \
            \t\tmov edx, 1\n \
            \t\tpop ebx\n \
            \t\tpop eax\n \
            \t\tcmp eax, ebx\n \
            \t\tcmovl ecx, edx\n \
            \t\tpush ecx\n"
            
def gequ():
    return "\t\tmov ecx, 0\n \
            \t\tmov edx, 1\n \
            \t\tpop ebx\n \
            \t\tpop eax\n \
            \t\tcmp eax, ebx\n \
            \t\tcmovge ecx, edx\n \
            \t\tpush ecx\n"
            
def lequ():
    return "\t\tmov ecx, 0\n \
            \t\tmov edx, 1\n \
            \t\tpop ebx\n \
            \t\tpop eax\n \
            \t\tcmp eax, ebx\n \
            \t\tcmovle ecx, edx\n \
            \t\tpush ecx\n"
            
def iff(addr):
    return f"\t\tpop eax\n \
             \t\ttest eax, eax\n \
             \t\tjz addr_{addr}\n"
             
def elsee(after_if_addr, after_else_addr):
    return f"\t\tjmp addr_{after_if_addr}\n \
            addr_{after_else_addr}:\n"
            
def whilee(addr):
    return f"addr_{addr}:\n"
            
def do(addr):
    return f"\t\tpop eax\n \
            \t\ttest eax, eax\n \
            \t\tjz addr_{addr}\n"
            
def end_while(addr):
    return f"\t\tjmp addr_{addr}\n"

def end_if_while(addr):
    return f"addr_{addr}:\n"
    
def printt(format_method):
    return f"\t\tpop eax\n \
            \t\tcinvoke printf, {format_method}, eax\n \
            \t\txor eax, eax\n"
            
def clear_asm_stack(asm_stack_size, local_stack_size):
    out = ''
    for _ in range(asm_stack_size + local_stack_size):
        out += "\t\tpop eax\n"
        
    if asm_stack_size > 0:
        out += "\t\txor eax, eax\n"
        
    return out

def copy():
    return "\t\tpop eax\n \
            \t\tpush eax\n \
            \t\tpush eax\n"
            
def pop():
    return "\t\tpop eax\n"
        