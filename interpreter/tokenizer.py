import re

js = """
var z = [1, 2, 3];

var x = {
    what: 5,
    name: "Timur"
};

x.name(haha);

function hello(a, what) {
    write('haha');
};

var x = function(n, a) {
    for (var i = 0; i > 5; i++) {
        n = i + 1;
    }

    if (n === 3 && n >= 4) {
        return false; 
    }
    return n / 5;
};

x();
"""

class Iter(object):
    def __init__(self):
        self.i = -1
        self.max_len = len(js) - 1

    def next(self):
        if self.i < self.max_len:
            self.i += 1
            self.char = js[self.i]
            return self.char
        return "EOF"


get = Iter()
tokens = []

def is_digit(char):
    return char.isdigit()

def is_regex_match(char, pattern):
    if pattern.match(char):
        return True
    return False

def is_alpha(char):
    pattern = re.compile("[a-zA-Z_$]")
    return is_regex_match(char, pattern)

def is_alpha_num(char):
    return is_regex_match(char, re.compile("^[a-zA-Z_$0-9]$"))

def is_white_space(char):
    pattern = re.compile('\s')
    return is_regex_match(char, pattern)

def is_newline(char):
    return char == '\n'

def is_operator(char):
    return char == "+" or char == "-" \
        or char == "=" or char == ">" or char == "<" \
        or char == "&" or char == "|" or char == "!" \
        or char == "*" or char == "/" or char == "%"

def is_square_bracket(char):
    return char == "[" or char == "]"

def is_comma(char):
    return char == ","

def is_colon(char):
    return char == ":"

def is_dot(char):
    return char == "."

def is_semicolon(char):
    return char == ';'

def is_dquote(char):
    return char == '"'

def is_squote(char):
    return char == "'"

def is_paren(char):
    return char == ")" or char == "("

def is_curly_bracket(char):
    return char == "{" or char == "}"

def handle_alpha(char, accumulator=""):
    accumulator += char
    char = get.next()
    if not is_alpha_num(char):
        if accumulator == "var":
            tokens.append(("VAR", "var"))
        elif accumulator == "function":
            tokens.append(("FUNCTION", "function"))
        elif accumulator == "return":
            tokens.append(("RETURN", "return"))
        elif accumulator == "if":
            tokens.append(("IF", "if"))
        elif accumulator == "else":
            tokens.append(("ELSE", "else"))
        elif accumulator == "for":
            tokens.append(("FOR", "for"))
        elif accumulator == "while":
            tokens.append(("WHILE", "while"))
        elif accumulator == "true":
            tokens.append(("BOOLEAN", "true"))
        elif accumulator == "false":
            tokens.append(("BOOLEAN", "false"))
        else:
            tokens.append(("ID", accumulator))
        handle_char(char)
    else:
        handle_alpha(char, accumulator)

def generate_black_hole(cond):
    def helper(char):
        char = get.next()
        if cond(char):
            helper(char)
        else:
            handle_char(char)
    return helper

def handle_white_space(char):
    func = generate_black_hole(lambda x: is_white_space(x))
    func(char)

def handle_newline(char):
    func = generate_black_hole(lambda x: is_newline(x))
    func(char)

def handle_comment(char):
    func = generate_black_hole(lambda x: x != '\n')
    func(char)

def operator_helper(cond, stop=None, token_name="OPERATOR"):
    def helper(char, accumulator=""):
        accumulator += char
        char = get.next()
        if not cond(char):
            tokens.append((token_name, accumulator))
            handle_char(char)
        else:
            if accumulator + char == stop:
                raise Exception("Syntax Error, token " + stop + " not allowed")
            else:
                helper(char, accumulator)
    return helper

def handle_digit(char, accumulator=""):
    func = operator_helper(lambda x: is_digit(x), token_name="NUMBER")
    func(char)

def handle_plus(char):
    func = operator_helper(lambda x: x == "+", "+++")
    func(char)

def handle_minus(char):
    func = operator_helper(lambda x: x == "-", "---")
    func(char)

def handle_equal(char):
    func = operator_helper(lambda x: x == "=", "====")
    func(char)

def handle_angles(char):
    if char == ">":
        stop = ">=="
    else:
        stop = "<=="
    func = operator_helper(lambda x: x == '=', stop)
    func(char)

def handle_and_or(char, accumulator=""):
    accumulator += char
    char = get.next()
    if accumulator == "&" or accumulator == "|":
        handle_and_or(char, accumulator)
    elif accumulator == "&&" or accumulator == "||":
        add_token("OPERATOR", accumulator, cont=True)
    else:
        raise Exception("Syntax Error: this token is not allowed: " + accumulator)

def handle_front_slash(char, accumulator=""):
    accumulator += char
    char = get.next()
    if char == "/":
        handle_comment(char)
    else:
        tokens.append(("OPERATOR", accumulator))
        handle_char(char)

def handle_quote(char, is_quote, accumulator=""):
    char = get.next()
    if not is_quote(char):
        if char == "EOF":
            raise Exception("String not closed")
        accumulator += char
        handle_quote(char, is_quote, accumulator)
    else:
        add_token("STRING", accumulator, cont=True)

def handle_multiply(char):
    add_token("OPERATOR", char, cont=True)

def handle_modulo(char):
    add_token("OPERATOR", char, cont=True)

def handle_not(char):
    add_token("OPERATOR", char, cont=True)

def handle_semicolon(char):
    add_token("SEMICOLON", char, cont=True)

def handle_comma(char):
    add_token("COMMA", char, cont=True)

def handle_colon(char):
    add_token("COLON", char, cont=True)

def handle_dot(char):
    add_token("DOT", char, cont=True)

def handle_operator(char):
    if char == '+':
        handle_plus(char)
    elif char == '-':
        handle_minus(char)
    elif char == "*":
        handle_multiply(char)
    elif char == "/":
        handle_front_slash(char)
    elif char == "%":
        handle_modulo(char)
    elif char == "=":
        handle_equal(char)
    elif char == ">" or char == "<":
        handle_angles(char)
    elif char == "&" or char == "|":
        handle_and_or(char)
    else:
        handle_not(char)


def handle_paren(char):
    if char == "(":
        add_token("LPAREN", char, cont=True)
    else:
        add_token("RPAREN", char, cont=True)


def handle_curly_bracket(char):
    if char == "{":
        add_token("LCURLY_BRACKET", char, cont=True)
    else:
        add_token("RCURLY_BRACKET", char, cont=True)


def handle_square_bracket(char):
    if char == "[":
        add_token("LSQUARE_BRACKET", char, cont=True)
    else:
        add_token("RSQUARE_BRACKET", char, cont=True)

def handle_char(char):
    if char == "EOF":
        return False
    if is_digit(char):
        handle_digit(char)
    elif is_alpha(char):
        handle_alpha(char)
    elif is_white_space(char):
        handle_white_space(char)
    elif is_newline(char):
        handle_newline(char)
    elif is_operator(char):
        handle_operator(char)
    elif is_semicolon(char):
        handle_semicolon(char)
    elif is_dquote(char):
        handle_quote(char, is_dquote)
    elif is_squote(char):
        handle_quote(char, is_squote)
    elif is_paren(char):
        handle_paren(char)
    elif is_curly_bracket(char):
        handle_curly_bracket(char)
    elif is_square_bracket(char):
        handle_square_bracket(char)
    elif is_comma(char):
        handle_comma(char)
    elif is_colon(char):
        handle_colon(char)
    elif is_dot(char):
        handle_dot(char)
    else:
        raise Exception("Syntax Error")

def add_token(name, value, cont=False):
    tokens.append((name, value))
    if cont:
        char = get.next()
        handle_char(char)

def tokenizer(js):
    char = get.next()
    handle_char(char)
    print tokens

tokenizer(js)
