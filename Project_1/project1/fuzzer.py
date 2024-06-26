from fuzzingbook.GeneratorGrammarFuzzer import *
import grammar
import random
import string
import re
import time


class Fuzzer:
    def __init__(self):
        # This function must not be changed.
        self.grammar = grammar.grammar
        self.setup_fuzzer()
        
    
    def setup_fuzzer(self):
        # This function may be changed.
        self.fuzzer = ProbabilisticGrammarFuzzer(self.grammar)
        self.count = 0
        self.state = dict()
        self.savepoints = list()
        self.start_time = time.time()
        self.elapsed_time = None
        self.fuzzer.max_nonterminals=20


    def fuzz_one_input(self) -> str:
        # This function should be implemented, but the signature may not change.

        self.elapsed_time = time.time() - self.start_time

        if self.elapsed_time >= 300:  # 300 seconds = 5 minutes
            # Delete the last half of the dictionary
            keys_to_delete = list(self.state.keys())[len(self.state) // 2:]
            for key in keys_to_delete:
                del self.state[key]

            self.start_time = time.time()  # Reset the start time
            # time.sleep(1)
            
        if self.count == 0 or self.count == 1:
            self.grammar.update({"<sql_statement>": [
              ("<create_table>", opts(prob=0.99)),
              "<select_statement>",
              "<insert_statement>",
              "<update_statement>",
              "<delete_statement>",
              "<commit_statement>",
              "<attach_statement>",
              "<detach_statement>",
              "<rollback_statement>",
              "<vacuum_statement>",
              "<create_index_statement>",
              "<drop_index_statement>",
              "<analyze_statement>",
              "<begin_statement>",
              "<pragma_statement>",
              "<savepoint_statement>",
              "<release_statement>",
              "<reindex_statement>"
          ]})
        
        else:
            self.grammar.update({"<sql_statement>": [
              "<create_table>",
              "<select_statement>",
              "<insert_statement>",
              "<update_statement>",
              "<delete_statement>",
              "<commit_statement>",
              "<attach_statement>",
              "<detach_statement>",
              "<rollback_statement>",
              "<vacuum_statement>",
              "<create_index_statement>",
              "<drop_index_statement>",
              "<analyze_statement>",
              "<begin_statement>",
              "<pragma_statement>",
              "<savepoint_statement>",
              "<release_statement>",
              "<reindex_statement>"
          ]})

        query = self.fuzzer.fuzz()
        if self.count > 0:
            checked_query = self.check_query(query)
        if query.startswith('CREATE TABLE'):
            self.add_table(query)

        if 'SELECT' in query:
            new_query = self.check_select_conditions(checked_query)
            new_query = self.check_between(checked_query)
            query = new_query
        
        if 'SAVEPOINT' in query:
            self.add_savepoint(query)

        if 'ROLLBACK' in query:
            query = self.replace_rollback(query)


        self.count += 1
        
        return query
    
    def check_select_conditions(self, query):
        if 'UNION' in query or 'JOIN' in query:
            # Split the query into parts based on the UNION keyword
            parts = [part.strip() for part in query.split('UNION')]

            # Get the columns from the SELECT statement in the first part
            if 'SELECT' in parts[0] and 'FROM' in parts[0]:
                        # Get the columns from the SELECT statement in the first part
                        select_index = parts[0].index('SELECT')
                        from_index = parts[0].index('FROM')
                        first_part_columns = parts[0][select_index + 6:from_index].split(',')

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
                    join_condition = parts[i][on_index+2:].strip()

                    # Split the condition based on the operator
                    operators = ['=', '<', '>', '<=', '>=', '!=', '<>']
                    for operator in operators:
                        if operator in join_condition:
                            join_condition = parts[i][on_index+2:].split(operator)
                    
                            # If the columns in the JOIN condition are not the same, make them the same
                            if len(join_condition) > 1:
                                if join_condition[0].strip() != join_condition[1].strip():
                                    parts[i] = parts[i].replace(join_condition[1], join_condition[0])

            
            # Return the modified query
            return ' UNION '.join(parts)
        else:
            return query

    def check_between(self, query):
        indexes = []
        query_tokens = query.split()

        if "BETWEEN" in query_tokens:
            # Find the index of "BETWEEN" or "NOT BETWEEN"
            for index, value in enumerate(query_tokens):
                if value == "BETWEEN":
                    indexes.append(index)
            # index = upper_tokens.index("BETWEEN")
            
            # Make sure there is a token to the right
            for index in indexes:
                if index + 1 < len(query_tokens):
                    literal = query_tokens[index + 1]
                    random_literal = ''.join(random.choices(string.ascii_letters + string.digits))

                    # Insert the random literal after the token to the right
                    try:
                        if ')' in query_tokens[index + 1]:
                            new_string = ''.join([char for char in query[index + 1] if char != ')'])
                            query_tokens[index + 1] = new_string
                            query_tokens.insert(index + 2, f"AND {random_literal})")

                        else:
                            
                            query_tokens.insert(index + 2, f"AND {random_literal}")
                    except:
                        if ')' in query_tokens[index + 1]:
                            new_string = ''.join([char for char in query[index + 1] if char != ')'])
                            query_tokens[index + 1] = new_string
                            query_tokens.append(f"AND {random_literal})")

                        else:
                            query_tokens.append(f"AND {random_literal}")

        # Join the modified tokens back into a string
        modified_query = ' '.join(query_tokens)
        return modified_query
    
    def add_table(self, query):
        # Extract table name and column names using regular expressions
        match = re.match(r"CREATE TABLE (\w+) \((.*?)\)", query)
        if match:
            table_name = match.group(1)
            columns = [col.strip() for col in match.group(2).split(',')]
            columns_dict = {pair.split()[0]: pair.split()[1] for pair in columns}
            
            # Store the information in the dictionary
            self.state[table_name] = columns_dict
        else:
            # Handle cases with a single column
            match = re.match(r"CREATE TABLE (\w+) \((\w+)\)", query)
            if match:
                table_name = match.group(1)
                columns = [match.group(2).strip()]

                columns_dict = {pair.split()[0]: pair.split()[1] for pair in columns}
                # Store the information in the dictionary
                self.state[table_name] = columns_dict

    def add_savepoint(self, query):

        # check if the query contains savepoint
        if 'SAVEPOINT' in query:
            # extract the name of the savepoint
            match = re.search(r'SAVEPOINT\s+(\w+)', query)
            if match:
                name = match.group(1)
                # check if the name is not empty
                if name:
                    # save the name in the list
                    self.savepoints.append(name)

    def check_query(self, query):
        table_name = re.findall(r'FROM\s+(\w+)', query)
        if table_name:
            table_name = table_name[0] 
            if table_name in self.state.keys():
                return query
            else:
                random_table_name = random.choice(list(self.state.keys()))
                query = query.replace(table_name, random_table_name)
        else:
            if query.startswith('CREATE TABLE'):
                table_name = re.findall(r'CREATE TABLE\s+(\w+)', query)
                if table_name:
                    table_name = table_name[0]
                    if table_name not in self.state.keys():
                        random_table_name = random.choice(list(self.state.keys()))
                        query = query.replace(table_name, random_table_name)
            elif query.startswith('INSERT'):
                table_name = re.findall(r'INSERT INTO\s+(\w+)', query)
                if table_name:
                    table_name = table_name[0]
                    if table_name not in self.state.keys():
                        random_table_name = random.choice(list(self.state.keys()))
                        query = query.replace(table_name, random_table_name)
            elif query.startswith('UPDATE'):
                table_name = re.findall(r'UPDATE\s+(\w+)', query)
                if table_name:
                    table_name = table_name[0]
                    if table_name not in self.state.keys():
                        random_table_name = random.choice(list(self.state.keys()))
                        query = query.replace(table_name, random_table_name)
            elif query.startswith('DELETE'):
                table_name = re.findall(r'DELETE FROM\s+(\w+)', query)
                if table_name:
                    table_name = table_name[0]
                    if table_name not in self.state.keys():
                        random_table_name = random.choice(list(self.state.keys()))
                        query = query.replace(table_name, random_table_name)
            elif query.startswith('ALTER TABLE'):
                table_name = re.findall(r'ALTER TABLE\s+(\w+)', query)
                if table_name:
                    table_name = table_name[0]
                    if table_name not in self.state.keys():
                        random_table_name = random.choice(list(self.state.keys()))
                        query = query.replace(table_name, random_table_name)
            elif query.startswith('DROP TABLE'):
                table_name = re.findall(r'DROP TABLE\s+(\w+)', query)
                if table_name:
                    table_name = table_name[0]
                    if table_name not in self.state.keys():
                        random_table_name = random.choice(list(self.state.keys()))
                        query = query.replace(table_name, random_table_name)
            elif query.startswith('CREATE INDEX'):
                table_name = re.findall(r'CREATE INDEX\s+(\w+)', query)
                if table_name:
                    table_name = table_name[0]
                    if table_name not in self.state.keys():
                        random_table_name = random.choice(list(self.state.keys()))
                        query = query.replace(table_name, random_table_name)
        return query
    
    def replace_rollback(self, query):
    
        # check if the query contains rollback
        if 'rollback' in query.lower():
            # extract the name of the rollback
            match = re.search(r"ROLLBACK\s+(\w+)", query, re.IGNORECASE)
            if match:
                name = match.group(1)
                # check if the name is not empty
                if name:
                    # choose a random savepoint from the list
                    if len(self.savepoints) > 0 :
                        savepoint = random.choice(self.savepoints)
                        # replace the rollback name with the savepoint
                        query = re.sub(r"ROLLBACK\s+\w+", f"ROLLBACK {savepoint}", query, re.IGNORECASE)
                    else:
                        query = f'SAVEPOINT {random.choices(string.ascii_lowercase, k=2)}'
                        self.add_savepoint(query)
                
            
        return query
    

if __name__ == "__main__":
    f = Fuzzer()
    f.fuzz_one_input()
    