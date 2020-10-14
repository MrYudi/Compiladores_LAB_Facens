import re

T_OP = "<OP, %s>" # =+-*/<>! >= <= || && ==
T_INT = "<numero, %s>" # numero (exemplo 3 4 9)
T_STRING = "<string, %s>" # esta dentro de aspas
T_IDENTIF = "<indice, %s>" # Exemplo.: int A ("A" seria o ID)
T_DELIMIT = "<DELIMIT, %s>" # (){}[]

T_KEYWORDS_END = "<KEYWORDS, sair>" # end

T_KEYWORDS_IF = "<KEYWORDS, passa>" # if
T_KEYWORDS_ELSEIF = "<KEYWORDS, repassa>" # elseif

T_KEYWORDS_FOR = "<KEYWORDS, papagaio>" # for 
T_KEYWORDS_EM = "<KEYWORDS, em>" # em

T_KEYWORDS_SWITCH = "<KEYWORDS, choices>" # switch
T_KEYWORDS_CASE = "<KEYWORDS, choice>" # case
T_KEYWORDS_DEFAULT = "<KEYWORDS, badchoice>" # default

T_KEYWORDS_PRINT = "<KEYWORDS, mostra>" # print

# Classe exception
class StopExecution(Exception):
    def _render_traceback_(self):
        pass

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
    
# Identificar primario
def afd_principal(token):
    
    if afd_operador(token): # Operadores
        return T_OP % token

    elif token == "mostra": # print
        return T_KEYWORDS_PRINT
        
    elif token == "sair":
        return T_KEYWORDS_END
    # -----------------------------------------
    # DELIMITADORES
    elif token in "(){}[]":
        return T_DELIMIT % token

    # -----------------------------------------
    # Switch
    elif token == "choices": 
        return T_KEYWORDS_SWITCH

    elif token == "choice": # Case
        return T_KEYWORDS_CASE

    elif token == "badchoice": # default
        return T_KEYWORDS_DEFAULT

    # -----------------------------------------
    # if
    elif token == "passa":
        return T_KEYWORDS_IF

    elif token == "repassa": # elseif
        return T_KEYWORDS_ELSEIF

    # -----------------------------------------
    # for
    elif token == "papagaio": 
        return T_KEYWORDS_FOR

    elif token == "em": # em
        return T_KEYWORDS_EM

    # -----------------------------------------
    elif afd_int(token):
        return T_INT % token
    
    elif afd_string(token):
        return T_STRING % token
    
    elif afd_identificador(token):
        return T_IDENTIF % token 
    
    else:
        raise ValueError('Valor inesperado')
        
    return None
    
# -----------------------------------------   
# Main

# Analise lexica
arquivo = open('exemplo.txt','r')
ln = 1
for l in arquivo.readlines():
    l = l.replace('\n','') # remove a quebra de linha
    tokens = []
    for token in l.split():
        try:
            #print(token)
            tokens.append(afd_principal(token))
        except Exception as e:
            print(tokens)
            print(str(e) + " na posição %i da linha %i" % (l.index(token), ln))
            raise StopExecution
    ln += 1

    print(tokens)

# Analise sintatica