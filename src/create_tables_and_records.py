from conexion.oracle_queries import OracleQueries

def create_tables(query: str):
    list_of_commands = query.split(";")

    oracle = OracleQueries(can_write=True)
    oracle.connect()

    for command in list_of_commands:
        if len(command.strip()) > 0:
            print(command)
            try:
                oracle.executeDDL(command)
                print("Successfully executed")
            except Exception as e:
                print(f"Error executing command: {e}")

def generate_records(query: str, sep: str = ';'):
    list_of_commands = query.split(sep)

    oracle = OracleQueries(can_write=True)
    oracle.connect()

    for command in list_of_commands:
        if len(command.strip()) > 0:
            print(command)
            try:
                oracle.write(command)
                print("Successfully executed")
            except Exception as e:
                print(f"Error inserting record: {e}")

def run():
    # scripts certos do projeto de pontos
    with open("../sql/create_tables.sql") as f:
        query_create = f.read()

    print("Creating tables...")
    create_tables(query=query_create)
    print("Tables successfully created!")

    with open("../sql/insert_records_func.sql") as f:
        query_generate_func = f.read()

    print("Generating FUNCIONARIOS records...")
    generate_records(query=query_generate_func)
    print("FUNCIONARIOS records successfully generated!")

    with open("../sql/insert_records_marc.sql") as f:
        query_generate_marc = f.read()

    print("Generating MARCACOES records...")
    generate_records(query=query_generate_marc)
    print("MARCACOES records successfully generated!")

if __name__ == "__main__":
    run()
