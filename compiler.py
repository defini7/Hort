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
OP_SHL = iota()
OP_SHR = iota()
OP_BIT_OR = iota()
OP_BIT_XOR = iota()
OP_BIT_AND = iota()
OP_BIT_NOT = iota()

OP_PUSH = iota() # push element to the stack
OP_DROP = iota() # removes all data from the stack
OP_PRINT = iota() # takes number from the stack and print in console

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
            continue
            
        if in_quotes:
            dump += ' ' + word
            continue
        
        if word == '+':
            tokens.append(Token(OP_PLUS))
        elif word == '-':
            tokens.append(Token(OP_MINUS))
        elif word == '*':
            tokens.append(Token(OP_MUL))
        elif word == '/':
            tokens.append(Token(OP_DIV))
        elif word == '|':
            tokens.append(Token(OP_BIT_OR))
        elif word == '&':
            tokens.append(Token(OP_BIT_AND))
        elif word == '!':
            tokens.append(Token(OP_BIT_NOT))
        elif word == '^':
            tokens.append(Token(OP_BIT_XOR))
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
                elif word == 'print':
                    tokens.append(Token(OP_PRINT))
                elif word == 'drop':
                    tokens.append(Token(OP_DROP))
                else:
                    assert False, 'Unexpected identifier'
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
        out.write("\tformat_int db '%d', 0\n")
        
        for t in tokens:
            if t.type == OP_STR:
                out.write("\tformat_str db '%s', 0\n")
                break
        
        str_count = 0
        for t in tokens:
            if t.type == OP_STR:
                t.id = str_count
                out.write(f"\ts_{t.id} db {t.value}, 0\n")
                str_count += 1
                
        out.write("section '.code' code readable writeable executable\n")
        out.write("\tstart:\n")
        
        local_stack = []
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
                out.write(f"\t\tpop ebx\n")
                out.write(f"\t\tpop eax\n")
                out.write(f"\t\tadd eax, ebx\n")
                out.write(f"\t\tpush eax\n")
                asm_stack_size -= 1
            elif t.type == OP_MINUS:
                out.write(f"\t\tpop ebx\n")
                out.write(f"\t\tpop eax\n") 
                out.write(f"\t\tsub eax, ebx\n")
                out.write(f"\t\tpush eax\n")
                asm_stack_size -= 1
            elif t.type == OP_BIT_XOR:
                out.write(f"\t\tpop ebx\n")
                out.write(f"\t\tpop eax\n")
                out.write(f"\t\txor eax, ebx\n")
                out.write(f"\t\tpush eax\n")
                asm_stack_size -= 1
            elif t.type == OP_BIT_OR:
                out.write(f"\t\tpop ebx\n")
                out.write(f"\t\tpop eax\n")
                out.write(f"\t\tor eax, ebx\n")
                out.write(f"\t\tpush eax\n")
                asm_stack_size -= 1
            elif t.type == OP_BIT_AND:
                out.write(f"\t\tpop ebx\n")
                out.write(f"\t\tpop eax\n")
                out.write(f"\t\tand eax, ebx\n")
                out.write(f"\t\tpush eax\n")
                asm_stack_size -= 1
            elif t.type == OP_BIT_NOT:
                out.write(f"\t\tpop eax\n")
                out.write(f"\t\tnot eax\n")
                out.write(f"\t\tpush eax\n")
                asm_stack_size -= 1
            elif t.type == OP_PRINT:
                out.write(f"\t\tpop eax\n")
                format_method = 'format_int' if local_stack.pop() == OP_INT else 'format_str'
                out.write(f"\t\tinvoke printf, {format_method}, eax\n")
                asm_stack_size -= 1
            elif t.type == OP_DROP:
                if asm_stack_size < 0:
                    assert False, 'Drop could not be called, because stack_size < 0'
                    
                for _ in range(asm_stack_size):
                    out.write("\t\tpop eax\n")
                    
                if asm_stack_size > 0:
                    out.write("\t\tmov eax, 0\n")
                
        out.write("\t\tinvoke ExitProcess, 0\n")
        out.write("section '.idata' data import readable\n")
        out.write("\tlibrary kernel, 'kernel32.dll', msvcrt, 'msvcrt.dll'\n")
        out.write("\timport kernel, ExitProcess, 'ExitProcess'\n")
        out.write("\timport msvcrt, printf, 'printf'\n")
        
        assert asm_stack_size == 0, f'Stack is not cleaned somewhere. Stack size: {asm_stack_size}'
        assert len(local_stack) == 0, f'Local stack is not cleaned somewhere. Stack size: {len(local_stack)}'
        
    subprocess.run(f'fasm {output_filename}')
    
if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
