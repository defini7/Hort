import sys
import subprocess

iota_count = -1
def iota(reset=False):
    global iota_count
    
    iota_count += 1
    
    if reset:
        temp = iota_count
        iota_count = 0
        return temp
    
    return iota_count

OP_PLUS = iota()
OP_MINUS = iota()
OP_MUL = iota()
OP_DIV = iota()
OP_INC = iota()
OP_DEC = iota()
OP_BIT_SHL = iota()
OP_BIT_SHR = iota()
OP_BIT_OR = iota()
OP_BIT_XOR = iota()
OP_BIT_AND = iota()
OP_BIT_NOT = iota()

OP_EQU = iota() # ==
OP_NEQU = iota() # !=
OP_LESS = iota() # <
OP_GREATER = iota() # >
OP_LEQU = iota() # <=
OP_GEQU = iota() # >=

OP_PUSH = iota() # push element to the stack
OP_DROP = iota() # removes all data from the stack
OP_COPY = iota() # gives last element from the stack
OP_PRINT = iota() # takes number from the stack and print in console
OP_IF = iota()
OP_WHILE = iota()
OP_DO = iota()
OP_ELSE = iota()
OP_END = iota()

OP_INT = iota()
OP_STR = iota(True)

class Token:
    def __init__(self, tok_type: int, value=None, tok_id=0):
        self.type = tok_type
        self.value = value
        self.id = tok_id

def parse(src: str):
    tokens: list[Token] = []
    
    in_quotes = False
    dump: str | None = ''
    
    for word in src.split():
        if word[len(word) - 1] == '"':
            in_quotes = False
            dump += ' ' + word
            tokens.append(Token(OP_STR, dump))
            dump = ''
            continue
            
        if in_quotes:
            dump += ' ' + word
            continue
        
        if word == '+': tokens.append(Token(OP_PLUS))
        elif word == '-': tokens.append(Token(OP_MINUS))
        elif word == '*': tokens.append(Token(OP_MUL))
        elif word == '/': tokens.append(Token(OP_DIV))
        elif word == '<<': tokens.append(Token(OP_BIT_SHL))
        elif word == '>>': tokens.append(Token(OP_BIT_SHR))
        elif word == '++': tokens.append(Token(OP_INC))
        elif word == '--': tokens.append(Token(OP_DEC))
        elif word == '|': tokens.append(Token(OP_BIT_OR))
        elif word == '&': tokens.append(Token(OP_BIT_AND))
        elif word == '!': tokens.append(Token(OP_BIT_NOT))
        elif word == '^': tokens.append(Token(OP_BIT_XOR))
        elif word == '==': tokens.append(Token(OP_EQU))
        elif word == '!=': tokens.append(Token(OP_NEQU))
        elif word == '<': tokens.append(Token(OP_LESS))
        elif word == '>': tokens.append(Token(OP_GREATER))
        elif word == '<=': tokens.append(Token(OP_LEQU))
        elif word == '>=': tokens.append(Token(OP_GEQU))
        else:
            if word[0] == '"':
                in_quotes = True
                dump += word
                continue
            
            if word.isdigit():
                tokens.append(Token(OP_INT, word))
            elif word.isalnum():
                if word.startswith('0x') or word.startswith('0b'):
                    word += word[1]
                    word = word.replace('0x', '')
                    word = word.replace('0b', '')
                    tokens.append(Token(OP_INT, word))
                elif word == 'print': tokens.append(Token(OP_PRINT))
                elif word == 'drop': tokens.append(Token(OP_DROP))
                elif word == 'copy': tokens.append(Token(OP_COPY))
                elif word == 'if': tokens.append(Token(OP_IF))
                elif word == 'while': tokens.append(Token(OP_WHILE))
                elif word == 'do': tokens.append(Token(OP_DO))
                elif word == 'else': tokens.append(Token(OP_ELSE))
                elif word == 'end': tokens.append(Token(OP_END))
                else: assert False, 'Unexpected identifier'
            else:
                assert False, f'Unhandled token: {word}'
            
    return tokens

def main(argc: int, argv: list[str]):
    assert argc >= 2, 'Please provide filename'
    
    with open(argv[1] + '.hort', 'r') as f:
        tokens = parse(f.read())
        
    output_filename = argv[1] + '.s'
    with open(output_filename, 'w') as out:
        out.write("format PE console\n")
        out.write("entry start\n")
        out.write("include 'INCLUDE\\win32a.inc'\n")
        out.write("section '.data' data readable writeable\n")
        out.write("\tformat_int db '%d', 10, 0\n")
        
        for t in tokens:
            if t.type == OP_STR:
                out.write("\tformat_str db '%s', 10, 0\n")
                break
        
        str_count = 0
        if_index = 0
        while_index = 1
        for i in range(len(tokens)):
            if tokens[i].type == OP_STR:
                tokens[i].id = str_count
                out.write(f"\ts_{tokens[i].id} db {tokens[i].value}, 0\n")
                str_count += 1
            elif tokens[i].type == OP_IF:
                tokens[i].id = if_index
                if_index += 1
            elif tokens[i].type == OP_WHILE:
                tokens[i].id = while_index
                while_index += 2
                
        out.write("section '.code' code readable writeable executable\n")
        out.write("\tstart:\n")
        
        local_stack = []
        if_while_stack = []
        asm_stack_size = 0
        
        for t in tokens:
            if t.type == OP_PUSH or t.type == OP_INT:
                out.write(f"\t\tpush {t.value}\n")
                local_stack.append(OP_INT)
                asm_stack_size += 1
            elif t.type == OP_STR:
                out.write(f"\t\tpush s_{t.id}\n")
                local_stack.append(OP_STR)
                asm_stack_size += 1
            elif t.type == OP_PLUS:
                out.write("\t\tpop ebx\n")
                out.write("\t\tpop eax\n")
                out.write("\t\tadd eax, ebx\n")
                out.write("\t\tpush eax\n")
                asm_stack_size -= 1
            elif t.type == OP_MINUS:
                out.write("\t\tpop ebx\n")
                out.write("\t\tpop eax\n") 
                out.write("\t\tsub eax, ebx\n")
                out.write("\t\tpush eax\n")
                asm_stack_size -= 1
            elif t.type == OP_INC:
                out.write("\t\tpop eax\n")
                out.write("\t\tinc eax\n")
                out.write("\t\tpush eax\n")
            elif t.type == OP_DEC:
                out.write("\t\tpop eax\n")
                out.write("\t\tdec eax\n")
                out.write("\t\tpush eax\n")
            elif t.type == OP_BIT_SHL:
                out.write("\t\tpop eax\n")
                out.write("\t\tshl eax\n")
                out.write("\t\tpush eax\n")
            elif t.type == OP_BIT_SHR:
                out.write("\t\tpop eax\n")
                out.write("\t\tshr eax\n")
                out.write("\t\tpush eax\n")
            elif t.type == OP_BIT_XOR:
                out.write("\t\tpop ebx\n")
                out.write("\t\tpop eax\n")
                out.write("\t\txor eax, ebx\n")
                out.write("\t\tpush eax\n")
                asm_stack_size -= 1
            elif t.type == OP_BIT_OR:
                out.write("\t\tpop ebx\n")
                out.write("\t\tpop eax\n")
                out.write("\t\tor eax, ebx\n")
                out.write("\t\tpush eax\n")
                asm_stack_size -= 1
            elif t.type == OP_BIT_AND:
                out.write("\t\tpop ebx\n")
                out.write("\t\tpop eax\n")
                out.write("\t\tand eax, ebx\n")
                out.write("\t\tpush eax\n")
                asm_stack_size -= 1
            elif t.type == OP_BIT_NOT:
                out.write("\t\tpop eax\n")
                out.write("\t\tnot eax\n")
                out.write("\t\tpush eax\n")
                asm_stack_size -= 1
            elif t.type == OP_EQU:
                out.write("\t\tmov ecx, 0\n")
                out.write("\t\tmov edx, 1\n")
                out.write("\t\tpop ebx\n")
                out.write("\t\tpop eax\n")
                out.write("\t\tcmp eax, ebx\n")
                out.write("\t\tcmove ecx, edx\n")
                out.write("\t\tpush ecx\n")
                local_stack.pop()
                local_stack.pop()
                asm_stack_size -= 1
            elif t.type == OP_NEQU:
                out.write("\t\tmov ecx, 0\n")
                out.write("\t\tmov edx, 1\n")
                out.write("\t\tpop ebx\n")
                out.write("\t\tpop eax\n")
                out.write("\t\tcmp eax, ebx\n")
                out.write("\t\tcmovne ecx, edx\n")
                out.write("\t\tpush ecx\n")
                local_stack.pop()
                local_stack.pop()
                asm_stack_size -= 1
            elif t.type == OP_GREATER:
                out.write("\t\tmov ecx, 0\n")
                out.write("\t\tmov edx, 1\n")
                out.write("\t\tpop ebx\n")
                out.write("\t\tpop eax\n")
                out.write("\t\tcmp eax, ebx\n")
                out.write("\t\tcmovg ecx, edx\n")
                out.write("\t\tpush ecx\n")
                local_stack.pop()
                local_stack.pop()
                asm_stack_size -= 1
            elif t.type == OP_LESS:
                out.write("\t\tmov ecx, 0\n")
                out.write("\t\tmov edx, 1\n")
                out.write("\t\tpop ebx\n")
                out.write("\t\tpop eax\n")
                out.write("\t\tcmp eax, ebx\n")
                out.write("\t\tcmovl ecx, edx\n")
                out.write("\t\tpush ecx\n")
                local_stack.pop()
                local_stack.pop()
                asm_stack_size -= 1
            elif t.type == OP_GEQU:
                out.write("\t\tmov ecx, 0\n")
                out.write("\t\tmov edx, 1\n")
                out.write("\t\tpop ebx\n")
                out.write("\t\tpop eax\n")
                out.write("\t\tcmp eax, ebx\n")
                out.write("\t\tcmovge ecx, edx\n")
                out.write("\t\tpush ecx\n")
                local_stack.pop()
                local_stack.pop()
                asm_stack_size -= 1
            elif t.type == OP_LEQU:
                out.write("\t\tmov ecx, 0\n")
                out.write("\t\tmov edx, 1\n")
                out.write("\t\tpop ebx\n")
                out.write("\t\tpop eax\n")
                out.write("\t\tcmp eax, ebx\n")
                out.write("\t\tcmovle ecx, edx\n")
                out.write("\t\tpush ecx\n")
                local_stack.pop()
                local_stack.pop()
                asm_stack_size -= 1
            elif t.type == OP_IF:
                out.write("\t\tpop eax\n")
                out.write("\t\ttest eax, eax\n")
                out.write(f"\t\tjz addr_{t.id}\n")
                if_while_stack.append(Token(OP_IF, t.id))
                asm_stack_size -= 1
            elif t.type == OP_ELSE:
                i = len(if_while_stack) - 2
                out.write(f"\t\tjmp addr_{if_while_stack[i].value + 1}\n")
                out.write(f"addr_{if_while_stack[i].value}:\n")
            elif t.type == OP_WHILE:
                out.write(f"addr_{t.id + 1}:\n")
                if_while_stack.append(Token(OP_WHILE, t.id))
            elif t.type == OP_DO:
                out.write("\t\tpop eax\n")
                out.write("\t\ttest eax, eax\n")
                out.write(f"\t\tjz addr_{if_while_stack[len(if_while_stack) - 1].value}\n")
                asm_stack_size -= 1
            elif t.type == OP_END:
                v = if_while_stack.pop()
                
                if v.type == OP_WHILE:
                    out.write(f"\t\tjmp addr_{v.value + 1}\n")
                
                out.write(f"addr_{v.value}:\n")
            elif t.type == OP_PRINT:
                out.write("\t\tpop eax\n")
                format_method = 'format_int' if local_stack.pop() == OP_INT else 'format_str'
                out.write(f"\t\tcinvoke printf, {format_method}, eax\n")
                out.write(f"\t\txor eax, eax\n")
                asm_stack_size -= 1
            elif t.type == OP_DROP:
                drop_error = ''
                if asm_stack_size < 0:
                    drop_error += f'\nDrop could not be called, because asm_stack_size < 0. Now: {asm_stack_size}'
                
                if len(local_stack) < 0:
                    drop_error += f'\nDrop could not be called, because len(local_stack) < 0. Now: {len(local_stack)}'
                    
                assert not drop_error, drop_error
                    
                for _ in range(asm_stack_size + len(local_stack)):
                    out.write("\t\tpop eax\n")
                    
                if asm_stack_size > 0:
                    out.write("\t\txor eax, eax\n")
                    
                asm_stack_size = 0
                local_stack.clear()
            elif t.type == OP_COPY:
                out.write("\t\tpop eax\n")
                out.write("\t\tpush eax\n")
                out.write("\t\tpush eax\n")
                local_stack.append(local_stack[len(local_stack) - 1])
                asm_stack_size += 1
                
        out.write("\t\tinvoke ExitProcess, 0\n")
        out.write("section '.idata' data import readable\n")
        out.write("\tlibrary kernel, 'kernel32.dll', msvcrt, 'msvcrt.dll'\n")
        out.write("\timport kernel, ExitProcess, 'ExitProcess'\n")
        out.write("\timport msvcrt, printf, 'printf'\n")
        
        stack_error = ''
        if asm_stack_size != 0:
            stack_error += f'Asm stack is not cleaned somewhere. Stack size: {asm_stack_size}\n'
            
        if len(local_stack) != 0:
            stack_error += f'Local stack is not cleaned somewhere. Stack size: {len(local_stack)}\n'
            
        if len(if_while_stack) != 0:
            stack_error += f'If is not closed with end somewhere. Not closed ifs: {len(if_while_stack)}\n'
        
        assert stack_error == '', stack_error
        
    subprocess.run(f'fasm {output_filename}')
    
if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
