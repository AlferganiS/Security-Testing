# Implement your grammar here in the `grammar` variable.
# You may define additional functions, e.g. for generators.
# You may not import any other modules written by yourself.
# That is, your entire implementation must be in `grammar.py`
# and `fuzzer.py`.

from fuzzingbook.ProbabilisticGrammarFuzzer import opts



   

grammar = {"<start>": ["<sql_statement>"],
    "<sql_statement>": [
        "<create_table>",
        "<select_statement>",
        "<insert_statement>",
        "<update_statement>",
        "<delete_statement>",
        "<alter_table_statement>",
        "<commit_statement>",
        "<attach_statement>",
        "<detach_statement>",
        "<rollback_statement>",
        "<vacuum_statement>",
        "<create_index_statement>",
        "<drop_index_statement>",
        "<drop_table_statement>"
        "<analyze_statement>",
        "<begin_statement>",
        "<pragma_statement>",
        "<savepoint_statement>",
        "<release_statement>",
        "<reindex_statement>"
    ],

    "<create_table>":[
        "CREATE TABLE <table_name> (<table_columns_def>)"
    ],

    "<select_statement>":[
        "<select_clause> <union_clause>",
        "<select_clause> <ordered_by_clause> <limit_clause> <union_clause>"
    ],

    "<insert_statement>":[
        "INSERT INTO <table_name> (<columns>) VALUES (<values>)"
    ],

    "<update_statement>":[
        "UPDATE <table_name> SET <column_value_pairs> <where_clause>"
    ],

    "<delete_statement>":[
        "DELETE FROM <table_name> <where_clause>"
    ],
    
    "<alter_table_statement>": [ 
        "ALTER TABLE <table_name> RENAME TO <table_name>",
        "ALTER TABLE <table_name> RENAME <column_name> TO <column_name>",
        "ALTER TABLE <table_name> RENAME COLUMN <column_name> TO <column_name>",
        "ALTER TABLE <table_name> ADD <table_column_def>",
        "ALTER TABLE <table_name> ADD COLUMN <table_column_def>",
        "ALTER TABLE <table_name> DROP COLUMN <column_name>"
        "ALTER TABLE <table_name> DROP <column_name>",
    ],

    "<commit_statement>":[
        "COMMIT"
        "END",
        "COMMIT TRANSACTION",
        "END TRANSACTION"
    ],

    "<attach_statement>": [  
        "ATTACH <literal> AS <identifier>",
        "ATTACH DATABASE <literal> AS <identifier>"
    ],

    "<detach_statement>": [  
        "DETACH <identifier>",
        "DETACH DATABASE <identifier>"
    ],

    "<rollback_statement>":[
        "ROLLBACK",
        "ROLLBACK TO <savepoint_name>",
        "ROLLBACK TO SAVEPOINT <savepoint_name>",
        "ROLLBACK TRANSACTION TO <savepoint_name>",
        "ROLLBACK TRANSACTION TO SAVEPOINT <savepoint_name>"
    ],

    "<vacuum_statement>":[
        "VACUUM",
        "VACUUM <identifier>",
        "VACUUM INTO <string_literal>",
        "VACUUM <identifier> INTO <string_literal>"
    ],

    "<create_index_statement>":[
        "CREATE INDEX <index_name> ON <table_name> (<columns>)"
    ],

    "<drop_index_statement>":[
        "DROP INDEX <index_name>"
    ],

    "<drop_table_statement>": [  
        "DROP TABLE <table_name>"
    ],

    "<analyze_statement>":[
        "ANALYZE",
        "ANALYZE <identifier>",
        "ANALYZE <index_name>"
    ],

    "<begin_statement>":[
        "BEGIN"
        "BEGIN DEFERRED",
        "BEGIN IMMEDIATE",
        "BEGIN EXCLUSIVE",
        "BEGIN TRANSACTION",
        "BEGIN DEFERRED TRANSACTION",
        "BEGIN IMMEDIATE TRANSACTION",
        "BEGIN EXCLUSIVE TRANSACTION"
    ],

    "<pragma_statement>": ["PRAGMA <schema-name-opt><pragma_name>"],

    "<savepoint_statement>":[
        "SAVEPOINT <savepoint_name>"
    ],

    "<release_statement>":[
        "RELEASE <savepoint_name>"
    ],

    "<reindex_statement>":[
        "REINDEX"
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
        ("<string_literal>", opts(pro=0.5)),
        ("<numeric_literal>", opts(prob=0.3)),
        "NULL",
        "CURRENT_DATE",
        "CURRENT_TIME",
        "CURRENT_TIMESTAMP"
    ],

    "<string_literal>":[
        ("<letter>", opts(prob=0.7)),
        "<string_literal><letter>"
    ],

    "<numeric_literal>":[
        ("<integer_literal>", opts(prob=0.6)),
        "<real_literal>"
    ],

    "<integer_literal>":[
        ("<digit>", opts(prob=0.8)),
        "<integer_literal><digit>"
    ],

    "<real_literal>":[
        "<integer_literal-1>.<integer_literal-2>"
    ],

    "<integer_literal-1>":[
        ("<digit-2>", opts(prob=0.9)),
        "<integer_literal-1><digit-1>"
    ],

    "<integer_literal-2>":[
        ("<digit-4>", opts(prob=0.9)),
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
        "<join_type> JOIN <table_reference> <join_condition>",
    ],

    "<join_condition>": [
        "ON <condition>",
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
        ("<letter>", opts(prob=0.8)),
        "<identifier><letter>",
        "<identifier><digit>"
    ],

    "<letter>":[
        ("a", opts(prob=0.15)), ("b", opts(prob=0.15)), ("c", opts(prob=0.15)), ("d", opts(prob=0.15)), "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",  "r", "s", "t", "u", "v", "w", "x", "y", "z",
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
    ],

    "<pragma_name>": [
            
        "<analysis_limit>", 
        "<application_id>", 
        "<auto_vacuum>", 
        "<automatic_index>", 
        "<busy_timeout>",
        "<cache_size>", 
        "<cache_spill>", 
        "<case_sensitive_like>", 
        "<cell_size_check>",
        "<checkpoint_fullfsync>", 
        "collation_list", 
        "compile_options", 
        "<count_changes>",
        "<data_store_directory>", 
        "data_version", 
        "database_list", 
        "<default_cache_size>",
        "<defer_foreign_keys>",
        "<empty_result_callbacks>", 
        "<encoding>", "<foreign_key_check>",
        "<foreign_key_list>", 
        "<foreign_keys>", 
        "freelist_count", 
        "<full_column_names>", 
        "<fullfsync>",
        "function_list", 
        "<hard_heap_limit>", 
        "<ignore_check_constraints>", 
        "<incremental_vacuum>",
        "<index_info>", 
        "<index_list>", 
        "<index_xinfo>", 
        "<integrity_check>", 
        "<journal_mode>",
        "<journal_size_limit>", 
        "<legacy_alter_table>", 
        "<legacy_file_format>", 
        "<locking_mode>",
        "<max_page_count>", 
        "<mmap_size>", 
        "module_list", 
        "<optimize>", 
        "page_count", 
        "<page_size>",
        "<parser_trace>", 
        "pragma_list", 
        "<query_only>", 
        "<quick_check>", 
        "<read_uncommitted>",
        "<recursive_triggers>", 
        "<reverse_unordered_selects>", 
        "<schema_version>", 
        "<secure_delete>",
        "<short_column_names>", 
        "shrink_memory", 
        "<soft_heap_limit>", 
        "stats", 
        "<synchronous>",
        "<table_info>", 
        "table_list", 
        "<table_list>", 
        "<table_xinfo>", 
        "<temp_store>",
        "<temp_store_directory>", 
        "<threads>", 
        "<trusted_schema>", 
        "<user_version>", 
        "<vdbe_addoptrace>",
        "<vdbe_debug>", 
        "<vdbe_listing>", 
        "<vdbe_trace>", 
        "<wal_autocheckpoint>", 
        "<wal_checkpoint>",
        "<writable_schema>"
    ],
    "<schema-name-opt>": [
            "",
            "SCHEMA <schema_name>"
    ],
        "<schema_name>": [
            "<identifier>"
    ],

    "<analysis_limit>": ["analysis_limit", "analysis_limit = <integer_literal>"],

    "<application_id>": ["application_id", "application_id = <integer_literal>"],

    "<auto_vacuum>": ["auto_vacuum", "auto_vacuum = <value1>"],

    "<automatic_index>": ["automatic_index", "automatic_index = <bool_value>"],

    "<busy_timeout>": ["busy_timeout", "busy_timeout =<integer_literal>"],

    "<cache_size>": ["cache_size<opt_cache_size>"],

    "<cache_spill>": ["cache_spill<opt_cache_spill>"],

    "<case_sensitive_like>": ["case_sensitive_like = 'a' LIKE 'a'"],

    "<cell_size_check>": ["cell_size_check<opt_cell_size_check>"],

    "<checkpoint_fullfsync>": ["checkpoint_fullfsync <opt_checkpoint_fullfsync>"],

    "<count_changes>": ["count_changes", "count_changes = <bool_value>"],

    "<data_store_directory>": ["data_store_directory", "data_store_directory = <string_literal>"],

    "<default_cache_size>": ["default_cache_size", "default_cache_size = <integer_literal>"],

    "<defer_foreign_keys>": ["defer_foreign_keys", "defer_foreign_keys = <bool_value>"],

    "<empty_result_callbacks>": ["empty_result_callbacks", "empty_result_callbacks = <bool_value>"],

    "<encoding>": ["PRAGMA encoding ", "encoding = 'UTF-8' ", "encoding = 'UTF-16' ", "encoding = 'UTF-16le' ", "encoding = 'UTF-16be'"],

    "<foreign_key_check>": ["foreign_key_check ", "foreign_key_check(<table_name>)"],

    "<foreign_key_list>": ["foreign_key_list(<table_name>)"],

    "<foreign_keys>": ["foreign_keys", "foreign_keys = <bool_value>"],

    "<full_column_names>": ["full_column_names ", "full_column_names = <bool_value>"],

    "<fullfsync>": ["fullfsync", "fullfsync = <bool_value>"],

    "<hard_heap_limit>": ["hard_heap_limit", "hard_heap_limit=<integer_literal>"],

    "<ignore_check_constraints>": ["ignore_check_constraints = <bool_value>"],

    "<incremental_vacuum>": ["incremental_vacuum(<integer_literal>)", "incremental_vacuum"],

    "<index_info>": ["index_info(<index_name>)"],

    "<index_list>": ["index_list(<table_name>)"],

    "<index_xinfo>": ["index_xinfo(<index_name>)"],

    "<integrity_check>": ["integrity_check ", "integrity_check(<integer_literal>)", "integrity_check(<table_name>)"],

    "<journal_mode>": ["journal_mode <opt_journal_mode> "],

    "<journal_size_limit>": ["journal_size_limit", "journal_size_limit = <integer_literal> "],

    "<legacy_alter_table>": ["legacy_alter_table", "legacy_alter_table = <bool_value>"],

    "<legacy_file_format>": ["legacy_file_format"],

    "<locking_mode>": ["locking_mode <opt_locking_mode> "],

    "<max_page_count>": ["max_page_count ", "max_page_count = <integer_literal>"],

    "<mmap_size>": ["mmap_size ", "mmap_size=<integer_literal>"],

    "<optimize>": ["optimize", "optimize(<mask>) "],

    "<page_size>": ["page_size ", "page_size = <integer_literal>"],

    "<parser_trace>": ["parser_trace = <bool_value> "],

    "<query_only>": ["query_only ", "query_only = <bool_value>"],

    "<quick_check>": ["quick_check ", "quick_check(<integer_literal>)", "quick_check(<table_name>)"],

    "<read_uncommitted>": ["read_uncommitted ", "read_uncommitted = <bool_value>"],

    "<recursive_triggers>": ["recursive_triggers ", "recursive_triggers = <bool_value>"],

    "<reverse_unordered_selects>": ["reverse_unordered_selects ", "reverse_unordered_selects = <bool_value>"],

    "<schema_version>": ["schema_version ", "schema_version = <integer_literal>  "],

    "<secure_delete>": ["secure_delete ", "secure_delete = <bool_value>", "secure_delete = FAST"],

    "<short_column_names>": ["short_column_names ", "short_column_names = <bool_value>"],

    "<soft_heap_limit>": ["soft_heap_limit", "soft_heap_limit=<integer_literal>"],

    "<synchronous>": ["synchronous ", "synchronous =<synchronous>"],

    "<table_info>": ["table_info(<table_name>)"],

    "<table_list>": ["table_list ", "table_list(<table_name>)"],

    "<table_xinfo>": ["table_xinfo(<table_name>)"],

    "<temp_store>": ["temp_store ", "temp_store = <temp_store>"],

    "<temp_store_directory>": ["temp_store_directory ", "temp_store_directory = '<string_literal>'"],

    "<threads>": ["threads ", "threads = <integer_literal>"],

    "<trusted_schema>": ["trusted_schema ", "trusted_schema = <bool_value>"],

    "<user_version>": ["user_version ", "user_version = <integer_literal> "],

    "<vdbe_addoptrace>": ["vdbe_addoptrace = <bool_value>"],

    "<vdbe_debug>": ["vdbe_debug = <bool_value>"],

    "<vdbe_listing>": ["vdbe_listing = <bool_value>"],

    "<vdbe_trace>": ["vdbe_trace = <bool_value>"],

    "<wal_autocheckpoint>": ["wal_autocheckpoint", "wal_autocheckpoint=<integer_literal>"],

    "<wal_checkpoint>": ["wal_checkpoint<opt_wal_checkpoint>"],

    "<writable_schema>": ["writable_schema = <bool_value>","writable_schema = RESET"],

    "<opt_wal_checkpoint>": ["", "(<passive_mode>)"],

    "<passive_mode>": ["PASSIVE", "FULL", "RESTART", "TRUNCATE"],

    "<temp_store>": ["0", "DEFAULT", "1", "FILE", "2", "MEMORY"],

    "<synchronous>": ["0", "OFF", "1", "NORMAL", "2", "FULL", "3", "EXTRA"],

    "<mask>": ["-1", "0x02", "0x10", "0x20", "0x40", "0x10000"],

    "<opt_locking_mode>": [" = NORMAL", " = EXCLUSIVE"],

    "<opt_journal_mode>": ["", " = DELETE", "= TRUNCATE", "= PERSIST", "= MEMORY", "= WAL", "= OFF"],

    "<opt_checkpoint_fullfsync>": ["", "= <bool_value>"],

    "<opt_cell_size_check>": ["", " = <bool_value>"],

    "<opt_cache_spill>": ["", "= <bool_value>", "= <integer_literal>"],

    "<opt_cache_size>": ["", "=<integer_literal>", "=-<integer_literal>"],

    "<bool_value>": ["true", "false"],

    "<value1>": ["0", "NONE", "1", "FULL", "2", "INCREMENTAL"]
        }




