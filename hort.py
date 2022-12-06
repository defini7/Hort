import sys
import subprocess

import constants
import operations
import utils

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
OP_POP = iota() # removes last element from the stack
OP_COPY = iota() # gives last element from the stack
OP_PRINT = iota() # takes number from the stack and print in console
OP_PRINTLN = iota()
OP_IF = iota()
OP_WHILE = iota()
OP_DO = iota()
OP_ELSE = iota()
OP_END = iota()

OP_INT = iota()
OP_STR = iota(True)

reserved_ops = {
    '+': OP_PLUS,
    '-': OP_MINUS,
    '*': OP_MUL,
    '/': OP_DIV,
    '++': OP_INC,
    '--': OP_DEC,
    '<<': OP_BIT_SHL,
    '>>': OP_BIT_SHR,
    '|': OP_BIT_OR,
    '^': OP_BIT_XOR,
    '&': OP_BIT_AND,
    '!': OP_BIT_NOT,
    '==': OP_EQU,
    '!=': OP_NEQU,
    '<': OP_LESS,
    '>': OP_GREATER,
    '<=': OP_LEQU,
    '>=': OP_GEQU
}

#reserved_keywords = {
#    'push': OP_PUSH,
#    'drop': OP_DROP,
#    'copy': OP_COPY,
#    'print': OP_PRINT,
#    'println': OP_PRINTLN,
#    'if': OP_IF,
#    'while': OP_WHILE,
#    'do': OP_DO,
#    'else': OP_ELSE, 
#    'end': OP_END
#}

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
        
        op = reserved_ops.get(word)
        if op is not None: tokens.append(Token(op))
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
                elif word == 'println': tokens.append(Token(OP_PRINTLN))
                elif word == 'drop': tokens.append(Token(OP_DROP))
                elif word == 'copy': tokens.append(Token(OP_COPY))
                elif word == 'pop': tokens.append(Token(OP_POP))
                elif word == 'if': tokens.append(Token(OP_IF))
                elif word == 'while': tokens.append(Token(OP_WHILE))
                elif word == 'do': tokens.append(Token(OP_DO))
                elif word == 'else': tokens.append(Token(OP_ELSE))
                elif word == 'end': tokens.append(Token(OP_END))
                else: assert False, 'Unexpected identifier'
            else:
                assert False, f'Unhandled token: {word}'
            
    return tokens

def main(argv: list[str], config: dict):    
    with open(argv[1] + '.hort', 'r') as f:
        tokens = parse(f.read())
        
    output_filename = argv[1] + '.s'
    
    config['cmd'] = [
        f'fasm {output_filename}'
    ]
    
    with open(output_filename, 'w') as out:
        out.write(constants.ASM_FILE_BEGIN)
        
        know_about_str = False
        know_about_int = False
        for t in tokens:
            if t.type == OP_STR and not know_about_str:
                out.write("\tformat_str db '%s', 0\n")
                know_about_str = True
            elif t.type == OP_INT and not know_about_int:
                out.write("\tformat_int db '%d', 0\n")
                know_about_int = True
                
            if know_about_int and know_about_str:
                break
            
        for t in tokens:
            if t.type == OP_PRINTLN:
                if know_about_str:
                    out.write("\tformat_str_n db '%s', 10, 0\n")
                if know_about_int:
                    out.write("\tformat_int_n db '%d', 10, 0\n")
                    
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
                
        out.write(constants.ASM_FILE_AFTER_BEGIN)
        
        local_stack = []
        if_while_stack = []
        asm_stack_size = 0
        
        for t in tokens:
            if t.type == OP_PUSH or t.type == OP_INT:
                out.write(operations.push(t.value))
                local_stack.append(OP_INT)
                asm_stack_size += 1
            elif t.type == OP_STR:
                out.write(operations.push(t))
                local_stack.append(OP_STR)
                asm_stack_size += 1
            elif t.type == OP_PLUS:
                out.write(operations.plus())
                asm_stack_size -= 1
            elif t.type == OP_MINUS:
                out.write(operations.minus())
                asm_stack_size -= 1
            elif t.type == OP_INC:
                out.write(operations.inc())
            elif t.type == OP_DEC:
                out.write(operations.dec())
            elif t.type == OP_BIT_SHL:
                out.write(operations.bit_shl())
            elif t.type == OP_BIT_SHR:
                out.write(operations.bit_shr())
            elif t.type == OP_BIT_XOR:
                out.write(operations.bit_xor())
                asm_stack_size -= 1
            elif t.type == OP_BIT_OR:
                out.write(operations.bit_or())
                asm_stack_size -= 1
            elif t.type == OP_BIT_AND:
                out.write(operations.bit_and())
                asm_stack_size -= 1
            elif t.type == OP_BIT_NOT:
                out.write(operations.bit_not())
                asm_stack_size -= 1
            elif t.type == OP_EQU:
                out.write(operations.equ())
                local_stack.pop()
                local_stack.pop()
                asm_stack_size -= 1
            elif t.type == OP_NEQU:
                out.write(operations.nequ())
                local_stack.pop()
                local_stack.pop()
                asm_stack_size -= 1
            elif t.type == OP_GREATER:
                out.write(operations.greater())
                local_stack.pop()
                local_stack.pop()
                asm_stack_size -= 1
            elif t.type == OP_LESS:
                out.write(operations.less())
                local_stack.pop()
                local_stack.pop()
                asm_stack_size -= 1
            elif t.type == OP_GEQU:
                out.write(operations.gequ())
                local_stack.pop()
                local_stack.pop()
                asm_stack_size -= 1
            elif t.type == OP_LEQU:
                out.write(operations.lequ())
                local_stack.pop()
                local_stack.pop()
                asm_stack_size -= 1
            elif t.type == OP_IF:
                out.write(operations.iff(t.id))
                if_while_stack.append(Token(OP_IF, t.id))
                asm_stack_size -= 1
            elif t.type == OP_ELSE:
                i = len(if_while_stack) - 2
                out.write(operations.elsee(if_while_stack[i].value + 1, if_while_stack[i].value))
            elif t.type == OP_WHILE:
                out.write(operations.whilee(t.id + 1))
                if_while_stack.append(Token(OP_WHILE, t.id))
            elif t.type == OP_DO:
                out.write(operations.do(if_while_stack[len(if_while_stack) - 1].value))
                asm_stack_size -= 1
            elif t.type == OP_END:
                v = if_while_stack.pop()
                
                if v.type == OP_WHILE:
                    out.write(operations.end_while(v.value + 1))
                
                out.write(operations.end_if_while(v.value))
            elif t.type == OP_PRINT:
                format_method = 'format_int' if local_stack.pop() == OP_INT else 'format_str'
                out.write(operations.printt(format_method))
                asm_stack_size -= 1
            elif t.type == OP_PRINTLN:
                format_method = 'format_int_n' if local_stack.pop() == OP_INT else 'format_str_n'
                out.write(operations.printt(format_method))
                asm_stack_size -= 1
            elif t.type == OP_DROP:
                utils.make_error(
                    (asm_stack_size > 0, f'Drop could not be called, because asm_stack_size <= 0. Now: {asm_stack_size}'),
                    (len(local_stack) > 0, f'Drop could not be called, because len(local_stack) <= 0. Now: {len(local_stack)}')
                )
        
                operations.clear_asm_stack(asm_stack_size, len(local_stack))
                    
                asm_stack_size = 0
                local_stack.clear()
            elif t.type == OP_COPY:
                out.write(operations.copy())
                local_stack.append(local_stack[len(local_stack) - 1])
                asm_stack_size += 1
            elif t.type == OP_POP:
                out.write(operations.pop())
                local_stack.pop()
                asm_stack_size -= 1
                
        out.write(constants.ASM_FILE_END)
        utils.make_error(
            (asm_stack_size == 0, f'Asm stack is not cleaned somewhere. Stack size: {asm_stack_size}'),
            (len(local_stack) == 0, f'Local stack is not cleaned somewhere. Stack size: {len(local_stack)}'),
            (len(if_while_stack) == 0, f'If is not closed with end somewhere. Not closed ifs: {len(if_while_stack)}')
        )
    
    for cmd in config['cmd']:
        subprocess.run(cmd)
    
    if config['run']:
        subprocess.run(f'./{argv[1]}')
    
if __name__ == '__main__':    
    assert len(sys.argv) >= 2, 'Usage: python3 hort.py [flags]\nFlags: -r'
    
    config = {
        'run': False
    }
    
    for arg in [sys.argv[i][2:] for i in range(2, len(sys.argv))]:
        config[arg] = True
    
    main(sys.argv, config)
