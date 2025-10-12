from model.funcionario import Funcionario
from conexion.oracle_queries import OracleQueries

class Controller_Funcionario:
    def __init__(self):
        pass

    def inserir_funcionario(self) -> Funcionario | None:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        id_func = int(input("ID do Funcionário: "))

        if self.verifica_existencia_funcionario(oracle, id_func):
            nome = input("Nome: ")
            cpf = input("CPF: ")
            cargo = input("Cargo: ")

            oracle.write(f"""
                insert into funcionario (id_func, nome, cpf, cargo)
                values ({id_func}, '{nome}', '{cpf}', '{cargo}')
            """)

            df = oracle.sqlToDataFrame(f"""
                select id_func, nome, cpf, cargo
                  from funcionario
                 where id_func = {id_func}
            """)

            novo = Funcionario(
                df.id_func.values[0],
                df.nome.values[0],
                df.cpf.values[0],
                df.cargo.values[0]
            )
            print(novo.to_string())
            return novo
        else:
            print(f"O id_func {id_func} já existe.")
            return None

    def atualizar_funcionario(self) -> Funcionario | None:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        id_func = int(input("ID do Funcionário que irá alterar: "))

        if not self.verifica_existencia_funcionario(oracle, id_func):
            novo_nome = input("Nome: ")
            novo_cargo = input("Cargo ")
            oracle.write(f"""
                update funcionario
                   set nome  = '{novo_nome}',
                       cargo = '{novo_cargo}'
                 where id_func = {id_func}
            """)

            df = oracle.sqlToDataFrame(f"""
                select id_func, nome, cpf, cargo
                  from funcionario
                 where id_func = {id_func}
            """)
            atualizado = Funcionario(
                df.id_func.values[0], 
                df.nome.values[0],
                df.cpf.values[0],
                df.cargo.values[0]
            )
            print(atualizado.to_string())
            return atualizado
        else:
            print(f"O id_func {id_func} não existe.")
            return None

    def excluir_funcionario(self) -> None:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        id_func = int(input("ID do Funcionário que irá excluir: "))

        if not self.verifica_existencia_funcionario(oracle, id_func):
            df = oracle.sqlToDataFrame(f"""
                select id_func, nome, cpf, cargo
                  from funcionario
                 where id_func = {id_func}
            """)
            oracle.write(f"delete from funcionario where id_func = {id_func}")
            excluido = Funcionario(
                df.id_func.values[0],
                df.nome.values[0],
                df.cpf.values[0],
                df.cargo.values[0]
            )
            print("Funcionário removido com sucesso!")
            print(excluido.to_string())
        else:
            print(f"O id_func {id_func} não existe.")

    def verifica_existencia_funcionario(self, oracle: OracleQueries, id_func: int) -> bool: # True se não existe
        df = oracle.sqlToDataFrame(f"""
            select id_func
              from funcionario
             where id_func = {id_func}
        """)
        return df.empty
