import re

T_OP = "OP" # =+-*/<>! >= <= || && ==
T_INT = "numero" # numero (exemplo 3 4 9)
T_STRING = "string" # esta dentro de aspas
T_IDENTIF = "indice" # Exemplo.: int A ("A" seria o ID)
T_DELIMIT = "DELIMIT" # (){}[]

T_KEYWORDS = "KEYWORDS"

T_KEYWORDS_END = "sair" # end

T_KEYWORDS_IF = "passa" # if
T_KEYWORDS_ELSEIF = "repassa" # elseif

T_KEYWORDS_FOR = "papagaio" # for 
T_KEYWORDS_EM = "em" # em

T_KEYWORDS_SWITCH = "choices" # switch
T_KEYWORDS_CASE = "choice" # case
T_KEYWORDS_DEFAULT = "badchoice" # default

T_KEYWORDS_PRINT = "mostra" # print

T_EOF = "EOF" # Fim

# -----------------------------------------   
# Classe exception
class StopExecution(Exception):
    def _render_traceback_(self):
        pass

# -----------------------------------------   
# Classe Token
class Token():
    
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        
    def __str__(self):
        return '<%s , %s>' % (self.tipo, self.valor)

# -----------------------------------------   
# LEXICA
# Identificar primario
def afd_principal(token):
    
    if afd_operador(token): # Operadores
        return Token(T_OP,token)

    elif token == T_KEYWORDS_PRINT: # print
        return Token(T_KEYWORDS, token)
        
    elif token == T_KEYWORDS_END:
        return Token(T_KEYWORDS,token)
    # -----------------------------------------
    # DELIMITADORES
    elif token in "(){}[]":
        return Token(T_DELIMIT,token) 

    # -----------------------------------------
    # Switch
    elif token == T_KEYWORDS_SWITCH: 
        return Token(T_KEYWORDS,token)

    elif token == T_KEYWORDS_CASE: # Case
        return Token(T_KEYWORDS,token)

    elif token == T_KEYWORDS_DEFAULT: # default
        return Token(T_KEYWORDS,token)

    # -----------------------------------------
    # if
    elif token == T_KEYWORDS_IF:
        return Token(T_KEYWORDS,token)

    elif token == T_KEYWORDS_ELSEIF: # elseif
        return Token(T_KEYWORDS,token)

    # -----------------------------------------
    # for
    elif token == T_KEYWORDS_FOR: 
        return Token(T_KEYWORDS,token)

    elif token == T_KEYWORDS_EM: # em
        return Token(T_KEYWORDS,token)

    # -----------------------------------------
    elif afd_int(token):
        return Token(T_INT,token) 
    
    elif afd_string(token):
        return Token(T_STRING,token)
    
    elif afd_identificador(token):
        return Token(T_IDENTIF,token)
    
    else:
        raise ValueError('Valor inesperado')
        
    return None

# Identificar secundario
def afd_operador(token):

    if token in "=+-*/<>!":
        return True
    elif token == "==":
        return True
    elif token == "&&":
        return True
    elif token == "||":
        return True
    elif token == "<=":
        return True
    elif token == ">=":
        return True
    elif token == "=<":
        token = "<="
        return True
    elif token == "=>":
        token = "=>"
        return True
    else:
        return False

def afd_int(token):
    try:
        token = int(token)
        return True
    except:
        return False
    
def afd_string(token):
    if token[0] == '"' and token[-1] == '"':
        if '"' not in token[1:-1]:
            return True
        else:
            raise ValueError('Aspas em um local inespeerado')
    else:
        return False
    
def afd_identificador(token):
    regex = re.compile('[a-zA-Z][a-zA-Z0-9]*')
    r = regex.match(token)
    if r is not None:
        if r.group() == token:
            return True
        else:
            return False
    else:
        return False
    
# -----------------------------------------      
# SINTATICA
class Parser():
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.token_atual = None
        
        self.proximo()
        
    # Proximo token
    def proximo(self):
        
        self.pos += 1
        
        if self.pos >= len(self.tokens): # Verificou todos Tokens?
            self.token_atual = Token(T_EOF) # Chegou no Fim
        else:    
            self.token_atual = self.tokens[self.pos] # Coloca o proximo

        return self.token_atual
    
    def erro(self):
        raise Exception('Erro de sintaxe.')    
        
    def use(self, tipo, valor=None):
                
        if self.token_atual.tipo != tipo:
            self.erro()
        elif valor is not None and self.token_atual.valor != valor:
            self.erro()
        else:
            print(self.token_atual)
            self.proximo()
        
    # Raiz
    # Acresentar outros sintaxe [IF, ELSE, FOR, CASE E ETC...]
    def statement(self):
        """
        statement ::= expr
        """

        print("E =")
        x = self.expr()
        print("= ", x)
               
    def expr(self):
        """
        expr ::= term ( <op +> | <op -> term )*
        """

        a = self.term()
        while self.token_atual.tipo == T_OP and self.token_atual.valor in ['+','-']:
            op = self.token_atual.valor
            self.use(T_OP)
            
            b = self.term()
            
            if op == "+":
                a += b
            elif op == "-":
                a -= b
            
        return a
      
    def term(self):
        """
        term ::= factor ( <op *> | <op /> factor)*
        """
        
        a = self.factor()
        while self.token_atual.tipo == T_OP and self.token_atual.valor in ['*','/']:
            op = self.token_atual.valor
            
            self.use(T_OP)
            b = self.factor()
            
            if op == "*":
                a *= b
            elif op == "/":
                a /= b
            
        return a          
            
    def factor(self):
        """
        factor ::= <id> | <int> | <par (> expr <par )>
        """
        
        if self.token_atual.tipo == T_INT:
            x = int(self.token_atual.valor)
            self.use(T_INT)
            return x
        elif self.token_atual.tipo == T_IDENTIF:
            self.use(T_IDENTIF)
        elif self.token_atual.tipo == T_DELIMIT and self.token_atual.valor == "(":
            self.use(T_DELIMIT, "(")
            x = self.expr()
            self.use(T_DELIMIT, ")")
            return x
        else:
            self.erro()

# -----------------------------------------   
# Main

# Analise lexica
print("LEXICA")
tokens = []
arquivo = open('Codigo\exemplo.txt','r')
ln = 1
for l in arquivo.readlines():
    l = l.replace('\n','') # remove a quebra de linha
    for token in l.split():
        try:
            #print(token)
            tokens.append(afd_principal(token))
        except Exception as e:
            #print(tokens)
            print(str(e) + " na posição %i da linha %i" % (l.index(token), ln))
            raise StopExecution
    ln += 1

    
print([str(t) for t in tokens])

# Analise sintatica
print("SINTATICA")
parser = Parser(tokens)
parser.statement()
