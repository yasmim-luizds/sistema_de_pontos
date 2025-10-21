from model.funcionario import Funcionario
from conexion.oracle_queries import OracleQueries

class Controller_Funcionario:
    def __init__(self):
        pass

    def inserir_funcionario(self) -> Funcionario | None:
        """
        Insere um funcionário gerando o ID via SEQUENCE.
        """
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Coleta dados (não pedimos mais o ID)
        nome = input("Nome: ").strip()
        cpf  = input("CPF (somente números): ").strip()
        cargo = input("Cargo: ").strip()

        # Gera novo ID pela SEQUENCE
        seq_df = oracle.sqlToDataFrame("""
            SELECT LABDATABASE.FUNCIONARIOS_CODIGO_FUNCIONARIO_SEQ.NEXTVAL AS id FROM DUAL
        """)
        novo_id = int(seq_df.iloc[0]["ID"])

        # Insere no schema/tabela corretos
        oracle.write(f"""
            INSERT INTO LABDATABASE.FUNCIONARIOS (CODIGO_FUNCIONARIO, NOME, CPF, CARGO)
            VALUES ({novo_id}, '{nome}', '{cpf}', '{cargo}')
        """)

        # Busca o registro inserido com aliases que casam com o modelo
        df = oracle.sqlToDataFrame("""
            SELECT 
                CODIGO_FUNCIONARIO AS id_func,
                NOME               AS nome,
                CPF                AS cpf,
                CARGO              AS cargo
            FROM LABDATABASE.FUNCIONARIOS
            WHERE CODIGO_FUNCIONARIO = :1
        """, [novo_id])

        novo = Funcionario(
            df.id_func.values[0],
            df.nome.values[0],
            df.cpf.values[0],
            df.cargo.values[0]
        )
        print("Funcionário inserido com sucesso!")
        print(novo.to_string())
        return novo

    def atualizar_funcionario(self) -> Funcionario | None:
        """
        Atualiza nome e cargo de um funcionário existente.
        """
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        id_func = int(input("ID do Funcionário que irá alterar: "))

        # Só atualiza se EXISTE (lembrando: verifica_existencia_funcionario -> True se NÃO existe)
        if not self.verifica_existencia_funcionario(oracle, id_func):
            novo_nome  = input("Nome: ").strip()
            novo_cargo = input("Cargo: ").strip()

            oracle.write("""
                UPDATE LABDATABASE.FUNCIONARIOS
                   SET NOME  = :1,
                       CARGO = :2
                 WHERE CODIGO_FUNCIONARIO = :3
            """, [novo_nome, novo_cargo, id_func])

            df = oracle.sqlToDataFrame("""
                SELECT 
                    CODIGO_FUNCIONARIO AS id_func,
                    NOME               AS nome,
                    CPF                AS cpf,
                    CARGO              AS cargo
                FROM LABDATABASE.FUNCIONARIOS
                WHERE CODIGO_FUNCIONARIO = :1
            """, [id_func])

            atualizado = Funcionario(
                df.id_func.values[0],
                df.nome.values[0],
                df.cpf.values[0],
                df.cargo.values[0]
            )
            print("Funcionário atualizado com sucesso!")
            print(atualizado.to_string())
            return atualizado
        else:
            print(f"O id_func {id_func} não existe.")
            return None

    def excluir_funcionario(self) -> None:
        """
        Exclui um funcionário existente.
        """
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        id_func = int(input("ID do Funcionário que irá excluir: "))

        # Só exclui se EXISTE
        if not self.verifica_existencia_funcionario(oracle, id_func):
            # Carrega dados antes de excluir (para exibir depois)
            df = oracle.sqlToDataFrame("""
                SELECT 
                    CODIGO_FUNCIONARIO AS id_func,
                    NOME               AS nome,
                    CPF                AS cpf,
                    CARGO              AS cargo
                FROM LABDATABASE.FUNCIONARIOS
                WHERE CODIGO_FUNCIONARIO = :1
            """, [id_func])

            oracle.write("""
                DELETE FROM LABDATABASE.FUNCIONARIOS
                WHERE CODIGO_FUNCIONARIO = :1
            """, [id_func])

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

    def verifica_existencia_funcionario(self, oracle: OracleQueries, id_func: int) -> bool:
        """
        Retorna True se NÃO existe (mantém semântica original do seu código).
        """
        df = oracle.sqlToDataFrame("""
            SELECT 1 AS existe
              FROM LABDATABASE.FUNCIONARIOS
             WHERE CODIGO_FUNCIONARIO = :1
        """, [id_func])
        return df.empty
