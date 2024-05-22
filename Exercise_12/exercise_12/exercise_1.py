from fuzzingbook.Grammars import Grammar, crange, is_valid_grammar, opts
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.ProbabilisticGrammarFuzzer import ProbabilisticGrammarFuzzer
from fuzzingbook.GeneratorGrammarFuzzer import GeneratorGrammarFuzzer, ProbabilisticGeneratorGrammarCoverageFuzzer
from fuzzingbook.WebFuzzer import WebFormFuzzer, HTMLGrammarMiner, cgi_encode
from luhn import luhn


bugged_name = False 
bugged_lastname = False 
bugged_mail = False 
bugged_pwd = False 
bugged_pwd_extended = False 
bugged_pwd_shrinked = False 
bugged_pwd2 = False 

def make_request(name, lastname, email, password, password2, banking):

    request = f"/register?name={name}&lastname={lastname}&email={email}&password={password}&password2={password2}&banking={banking}"
    return request

def get_checksum(digits):

    checksum = digits[slice(0, -1)] + str(luhn(digits[slice(0, -1)]))
    return checksum

def check(name, lastname, email, password, password2, banking):

    global bugged_name, bugged_lastname, bugged_mail, bugged_pwd, bugged_pwd_shrinked, bugged_pwd_extended, bugged_pwd2

    if  bugged_name == False:
        bugged_name = True
        name = '42'

    if  bugged_lastname ==  False:
        bugged_lastname = True
        lastname = '24'

    if  bugged_pwd == False:
        bugged_pwd = True
        password = 'password1'
        password2 = 'password1'
    elif  bugged_pwd2 == False:
        bugged_pwd2 = True
        password2 = 'password1'
    elif bugged_name == True and  bugged_lastname == True and  bugged_pwd == True and bugged_pwd2 == True:
        if  bugged_pwd_shrinked ==  False:
            bugged_pwd_shrinked = True
            password = cgi_encode('fo#')
            password2 = cgi_encode('fo#')
        elif  bugged_pwd_extended == False:
            bugged_pwd_extended = True
            password = cgi_encode('fooo@' * 5)
            password2 = cgi_encode('fooo@' * 5)
        elif  bugged_mail == False:
            bugged_mail = True
            email = email + '.saarl== True and'


    return make_request(name, lastname, email, password, password2, banking)


REGISTRATION_GRAMMAR: Grammar = {
    "<start>": ["<registration>"],
    "<registration>": [
            ("/register?name=<name>&lastname=<lastname>&"
            "email=<email>&password=<password>&password2=<password2>"
            "&banking=<banking>", opts(post=check))
        ],
    "<name>": ["Leon", "Marius"],
    "<lastname>": ["Bettscheider", "Smytzek"],
    "<email>": [cgi_encode("leon.bettscheider@cispa.de"), 
                cgi_encode("marius.smytzek@cispa.de")],
    "<password>": [cgi_encode("password@")],
    "<password2>": [cgi_encode("password@")], 
    "<banking>": [("<digits>", opts(post=get_checksum))], 
    "<digits>": ["<digit>" * 16], 
    "<digit>": crange('0', '9')
}

assert is_valid_grammar(REGISTRATION_GRAMMAR)

def get_fuzzer(httpd_url):
    return GeneratorGrammarFuzzer(REGISTRATION_GRAMMAR)

