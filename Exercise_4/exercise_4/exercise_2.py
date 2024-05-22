"""
Use this file to implement your solution for exercise 4-2
"""


from fuzzingbook.Grammars import srange, opts, is_valid_grammar
from fuzzingbook.GeneratorGrammarFuzzer import GeneratorGrammarFuzzer
import string
import random

def generate_country_code():

    return random.choice(iban_cc_len)


def generate_valid_iban(Country_code, check_digit, b_ban):
    # Randomly select a country code and its length
    selected_country = generate_country_code()
    country_code = selected_country[0]
    iban_length = selected_country[1]

    # Generate random BBAN with the remaining length
    bban_length = iban_length - len(country_code) - 2  # Subtracting 2 for check digits
    bban = generate_random_bban(bban_length)

    # Combine country code, check digits, and BBAN to form the complete IBAN
    iban = f"{country_code}{check_digit}{bban}"

    return iban

def generate_random_bban(length):
    # Generate a random BBAN with the specified length
    return ''.join(random.choice('0123456789') for _ in range(length))

def calculate_check_digits(iban):
    country_code = iban[:2]

    for t in iban_cc_len:
        if t[0] == country_code:
            expected_length = t[1]

    if len(iban) != expected_length:
        raise ValueError("Invalid IBAN length for country {}".format(country_code))
    
    # Replace check digits by 00
    modified_iban = iban[:2] + '00' + iban[4:]

    # Move the four initial characters to the end
    modified_iban = modified_iban[4:] + modified_iban[:4] 

    # Replace letters with digits
    digit_iban = ""
    for char in modified_iban:
        if char.isalpha():
            digit_iban += str(ord(char.upper()) - ord('A') + 10)
        else:
            digit_iban += char

                
    # Convert to integer and Calculate mod-97 then subtract
    new_number = int(digit_iban)
    remainder = new_number % 97
    check_digits = 98 - remainder

    if len(str(check_digits)) < 2:
        check_digits = '0' + str(check_digits)
    else:
        check_digits = str(check_digits)

    return country_code + check_digits + iban[4:]
    
iban_cc_len = [("AL", 28), ("AD", 24), ("AT", 20), ("AZ", 28), ("BH", 22), ("BY", 28), ("BE", 16), 
               ("BA", 20), ("BR", 29), ("BG", 22), ("CR", 22), ("HR", 21), ("CY", 28), ("CZ", 24), 
               ("DK", 18), ("DO", 28), ("SV", 28), ("EE", 20), ("FO", 18), ("FI", 18), ("FR", 27), 
               ("GE", 22), ("DE", 22), ("GI", 23), ("GR", 27), ("GL", 18), ("GT", 28), ("HU", 28), 
               ("IS", 26), ("IQ", 23), ("IE", 22), ("IL", 23), ("IT", 27), ("JO", 30), ("KZ", 20), 
               ("XK", 20), ("KW", 30), ("LV", 21), ("LB", 28), ("LI", 21), ("LT", 20), ("LU", 20), 
               ("MK", 19), ("MT", 31), ("MR", 27), ("MU", 30), ("MD", 24), ("MC", 27), ("ME", 22), 
               ("NL", 18), ("NO", 15), ("PK", 24), ("PS", 29), ("PL", 28), ("PT", 25), ("QA", 29), 
               ("RO", 24), ("LC", 32), ("SM", 27), ("ST", 25), ("SA", 24), ("RS", 22), ("SC", 31), 
               ("SK", 24), ("SI", 19), ("ES", 24), ("SE", 24), ("CH", 21), ("TL", 23), ("TN", 24), 
               ("TR", 26), ("UA", 29), ("AE", 23), ("GB", 22), ("VA", 22), ("VG", 24)]

IBAN_GRAMMAR = {
    "<start>": [("<iban>", opts(post=calculate_check_digits))],
    "<iban>": [("<country_code><check_digits><bban>", opts(post=generate_valid_iban))],
    "<country_code>": ["<letter><letter>"],
    "<check_digits>": ["<digit><digit>"],
    "<bban>": ["<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
    "<letter>": srange(string.ascii_uppercase),
    "<digit>": srange(string.digits),
}

def check_select_conditions(query):
    # Split the query into parts based on the UNION keyword
    parts = [part.strip() for part in query.split('UNION')]

    # Get the columns from the SELECT statement in the first part
    first_part_columns = parts[0][parts[0].index('SELECT')+6:parts[0].index('FROM')].split(',')

    # Check the columns in the SELECT statements of the other parts
    for i in range(1, len(parts)):
        select_index = parts[i].index('SELECT')
        from_index = parts[i].index('FROM')
        columns = parts[i][select_index+6:from_index].split(',')
        
        # If the columns are not the same as in the first part, replace them
        if columns != first_part_columns:
            parts[i] = parts[i].replace(','.join(columns), ','.join(first_part_columns))

    # Check the columns in the JOIN condition, if it exists
    for i in range(len(parts)):
        if 'JOIN' in parts[i]:
            on_index = parts[i].index('ON')
            join_condition = parts[i][on_index+2:].split('=')
            
            # If the columns in the JOIN condition are not the same, make them the same
            if len(join_condition) > 1:
                if join_condition[0].strip() != join_condition[1].strip():
                    parts[i] = parts[i].replace(join_condition[1], join_condition[0])

    # Return the modified query
    return ' UNION '.join(parts)

# import sys
# sys.setrecursionlimit(500)  # Set an appropriate limit

grammar = {"<start>": ["<sql_statement>"],
          "<sql_statement>": [
              "<create_table>",
              ("<select_statement>", opts(post=check_select_conditions)),
              "<insert_statement>",
              "<update_statement>",
              "<delete_statement>",
              "<commit_statement>",
              "<rollback_statement>",
              "<vacuum_statement>",
              "<create_index_statement>",
              "<drop_index_statement>",
              "<analyze_statement>",
              "<begin_statement>",
              "<savepoint_statement>",
              "<release_statement>",
              "<reindex_statement>"
          ],

           "<create_table>":[
               "CREATE TABLE <table_name> (<table_columns_def>);"
           ],

           "<select_statement>":[
            "<select_clause> <union_clause>",
            "<select_clause> <ordered_by_clause> <limit_clause> <union_clause>"
           ],

           "<insert_statement>":[
               "INSERT INTO <table_name> (<columns>) VALUES (<values>);"
           ],

           "<update_statement>":[
               "UPDATE <table_name> SET <column_value_pairs> <where_clause>;"
           ],

           "<delete_statement>":[
               "DELETE FROM <table_name> <where_clause>;"
           ],

           "<commit_statement>":[
               "COMMIT;"
           ],

           "<rollback_statement>":[
               "ROLLBACK;"
           ],

           "<vacuum_statement>":[
               "VACUUM;"
           ],

           "<create_index_statement>":[
               "CREATE INDEX <index_name> ON <table_name> (<columns>);"
           ],

           "<drop_index_statement>":[
               "DROP INDEX <index_name>;"
           ],

           "<analyze_statement>":[
               "ANALYZE;"
           ],

           "<begin_statement>":[
               "BEGIN;"
           ],

           "<savepoint_statement>":[
               "SAVEPOINT <savepoint_name>;"
           ],

           "<release_statement>":[
               "RELEASE <savepoint_name>;"
           ],

           "<reindex_statement>":[
               "REINDEX;"
           ],

           "<table_name>":[
               "<identifier>"
           ],

           "<columns>":[
               "*",
               "<column_name>",
               "<columns>, <column_name>"
           ],

           "<column_name>":[
               "<identifier>"
           ],

           "<table_columns_def>":[
               "<table_column_def>",
               "<table_columns_def>, <table_column_def>"
           ],

           "<table_column_def>":[
               "<column_name> <data_type>"
           ],

           "<data_type>":[
               "TEXT",
               "INTEGER",
               "REAL",
               "BLOB"
           ],

           "<values>":[
               "<literal>",
               "<values>, <literal>"
           ],

           "<literal>":[
               "<string_literal>",
               "<numeric_literal>",
               "NULL",
               "CURRENT_DATE",
               "CURRENT_TIME",
               "CURRENT_TIMESTAMP"
           ],

           "<string_literal>":[
                "<letter>",
                "<string_literal><letter>"
           ],

           "<numeric_literal>":[
                "<integer_literal>",
                "<real_literal>"
           ],

           "<integer_literal>":[
                "<digit>",
                "<integer_literal><digit>"
           ],

           "<real_literal>":[
                "<integer_literal-1>.<integer_literal-2>"
           ],

           "<integer_literal-1>":[
                "<digit-2>",
                "<integer_literal-1><digit-1>"
           ],

           "<integer_literal-2>":[
                "<digit-4>",
                "<integer_literal-2><digit-3>"
           ],

    
           "<condition>":[
                "<column_name> <operator> <literal>",
                "<condition> AND <condition>",
                "<condition> OR <condition>",
                "(<condition>)" 
           ],
           "<select_clause>": [
                "SELECT <columns> FROM <table_reference> <join_clauses> <where_clause>",
            ],
            "<union_clause>": [
                "UNION <select_clause>",
                ""  # Represents an optional empty clause
            ],

           "<ordered_by_clause>":[
                "ORDER BY <column_name>",
                "" 
           ],

           "<limit_clause>":[
                "LIMIT <integer_literal>",
                "" 
           ],

           "<where_clause>": [
                "WHERE <condition>",
                ""  # Represents an optional empty clause
            ],
            
            "<join_clauses>": [
                "<join_clause>",
                "<join_clauses> <join_clause>",
                ""  # Represents an optional empty clause
            ],
            "<join_clause>": [
                "<join_type> JOIN <table_reference> ON <condition>",
            ],
            "<join_type>": [
                "INNER",
                "LEFT",
                "RIGHT",
                "FULL"
            ],
            "<table_reference>": [
                "<table_name>",
                "<table_name> AS <alias>"
                # ,"<table_reference> <join_clauses>"
            ],

           "<column_value_pairs>":[
                "<column_value_pair>",
                "<column_value_pairs>, <column_value_pair>"
           ],

           "<column_value_pair>":[
                "<column_name> = <string_literal>"
           ],


           "<operator>":[
                "=",
                "!=",
                "<",
                ">",
                "<=",
                ">=",
                "AND",
                "OR",
                "LIKE",
                "IS",
                "IN",
                "BETWEEN",
                "NOT LIKE",
                "NOT IN",
                "NOT BETWEEN"
           ],

           "<identifier>":[
                "<letter>",
                "<identifier><letter>",
                "<identifier><digit>"
           ],

           "<letter>":[
                "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",  "r", "s", "t", "u", "v", "w", "x", "y", "z",
                "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
           ],

           "<digit>":[
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
           ],

           "<digit-1>":[
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
           ],

           "<digit-2>":[
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
           ],

           "<digit-3>":[
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
           ],

           "<digit-4>":[
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
           ],

           "<index_name>":[
                "<identifier>"
           ],

           "<savepoint_name>":[
                "<identifier>"
           ],

           "<alias>":[
                "<identifier>"
           ]
          }

assert is_valid_grammar(IBAN_GRAMMAR)

if __name__ == '__main__':
    fuzzer = GeneratorGrammarFuzzer(grammar)
    for _ in range(1000):
        print(fuzzer.fuzz())
