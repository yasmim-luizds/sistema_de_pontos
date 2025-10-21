from model.marcacao import Marcacao
from conexion.oracle_queries import OracleQueries

class Controller_Marcacao:
    def __init__(self):
        pass

    def inserir_marcacao(self) -> Marcacao | None:
        """
        Insere um período de marcação (entrada e saída) para um funcionário existente.
        No banco grava em LABDATABASE.MARCACOES (com entrada/saida).
        Em Python, cria dois objetos Marcacao: entrada (E) e saída (S).
        Retorna o objeto de ENTRADA para manter a assinatura.
        """
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        id_func = int(input("ID do Funcionário (existente): "))

        # Verifica se o funcionário existe (True se NÃO existe)
        if self.verifica_existencia_funcionario(oracle, id_func):
            print(f"O ID do funcionário {id_func} não existe. Cadastre o funcionário primeiro.")
            return None

        data_marc    = input("Data (DD-MM-YYYY): ").strip()
        hora_ent     = input("Hora de ENTRADA (HH:MM): ").strip()
        hora_sai     = input("Hora de SAÍDA   (HH:MM): ").strip()

        # 1) próximo ID da sequence
        seq_df = oracle.sqlToDataFrame("""
            SELECT LABDATABASE.MARCACOES_CODIGO_MARCACAO_SEQ.NEXTVAL AS id FROM DUAL
        """)
        novo_id = int(seq_df.iloc[0]["ID"])

        # 2) Insere no schema/colunas corretos
        oracle.write("""
            INSERT INTO LABDATABASE.MARCACOES
                (CODIGO_MARCACAO, DATA_MARCACAO, HORA_ENTRADA, HORA_SAIDA, CODIGO_FUNCIONARIO)
            VALUES
                (:1,
                 TO_DATE(:2,'DD-MM-YYYY'),
                 TO_DATE(:2 || ' ' || :3, 'DD-MM-YYYY HH24:MI'),
                 TO_DATE(:2 || ' ' || :4, 'DD-MM-YYYY HH24:MI'),
                 :5)
        """, [novo_id, data_marc, hora_ent, hora_sai, id_func])

        # 3) Carrega o registro inserido
        df = oracle.sqlToDataFrame("""
            SELECT
                CODIGO_MARCACAO                      AS id_marc,
                CODIGO_FUNCIONARIO                   AS id_func,
                TO_CHAR(DATA_MARCACAO, 'DD-MM-YYYY') AS data_marc,
                TO_CHAR(HORA_ENTRADA,  'HH:MI')      AS hora_ent,
                TO_CHAR(HORA_SAIDA,    'HH:MI')      AS hora_sai
            FROM LABDATABASE.MARCACOES
            WHERE CODIGO_MARCACAO = :1
        """, [novo_id])

        # 4) Mapeia em dois objetos "por evento"
        marc_E = Marcacao(
            id_marc=df.id_marc.values[0],
            id_func=df.id_func.values[0],
            data_marc=df.data_marc.values[0],
            hora_marc=df.hora_ent.values[0],
            tipo="E"
        )
        marc_S = Marcacao(
            id_marc=df.id_marc.values[0],
            id_func=df.id_func.values[0],
            data_marc=df.data_marc.values[0],
            hora_marc=df.hora_sai.values[0],
            tipo="S"
        )

        print("Marcações inseridas com sucesso (Entrada e Saída):")
        print("  ", marc_E.to_string())
        print("  ", marc_S.to_string())

        # Mantém a assinatura retornando a entrada
        return marc_E

    def atualizar_marcacao(self) -> Marcacao | None:
        """
        Atualiza data, hora de entrada e hora de saída de um período existente.
        Retorna o objeto de ENTRADA (imprime também o de SAÍDA).
        """
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        id_marc = int(input("ID da Marcação (período) que irá alterar: "))

        # Só atualiza se EXISTE (lembrando: True se NÃO existe)
        if not self.verifica_existencia_marcacao(oracle, id_marc):
            nova_data     = input("Nova Data (DD-MM-YYYY): ").strip()
            nova_hora_ent = input("Nova Hora de ENTRADA (HH:MM): ").strip()
            nova_hora_sai = input("Nova Hora de SAÍDA   (HH:MM): ").strip()

            oracle.write("""
                UPDATE LABDATABASE.MARCACOES
                   SET DATA_MARCACAO = TO_DATE(:1,'DD-MM-YYYY'),
                       HORA_ENTRADA  = TO_DATE(:1 || ' ' || :2, 'DD-MM-YYYY HH24:MI'),
                       HORA_SAIDA    = TO_DATE(:1 || ' ' || :3, 'DD-MM-YYYY HH24:MI')
                 WHERE CODIGO_MARCACAO = :4
            """, [nova_data, nova_hora_ent, nova_hora_sai, id_marc])

            df = oracle.sqlToDataFrame("""
                SELECT
                    CODIGO_MARCACAO                      AS id_marc,
                    CODIGO_FUNCIONARIO                   AS id_func,
                    TO_CHAR(DATA_MARCACAO, 'DD-MM-YYYY') AS data_marc,
                    TO_CHAR(HORA_ENTRADA,  'HH:MI')      AS hora_ent,
                    TO_CHAR(HORA_SAIDA,    'HH:MI')      AS hora_sai
                FROM LABDATABASE.MARCACOES
                WHERE CODIGO_MARCACAO = :1
            """, [id_marc])

            marc_E = Marcacao(
                id_marc=df.id_marc.values[0],
                id_func=df.id_func.values[0],
                data_marc=df.data_marc.values[0],
                hora_marc=df.hora_ent.values[0],
                tipo="E"
            )
            marc_S = Marcacao(
                id_marc=df.id_marc.values[0],
                id_func=df.id_func.values[0],
                data_marc=df.data_marc.values[0],
                hora_marc=df.hora_sai.values[0],
                tipo="S"
            )

            print("Marcação atualizada com sucesso!")
            print("  ", marc_E.to_string())
            print("  ", marc_S.to_string())
            return marc_E
        else:
            print(f"O ID da marcação {id_marc} não existe.")
            return None

    def excluir_marcacao(self) -> None:
        """
        Exclui um período de marcação existente.
        """
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        id_marc = int(input("ID da Marcação (período) que irá excluir: "))

        # Só exclui se EXISTE
        if not self.verifica_existencia_marcacao(oracle, id_marc):
            df = oracle.sqlToDataFrame("""
                SELECT
                    CODIGO_MARCACAO                      AS id_marc,
                    CODIGO_FUNCIONARIO                   AS id_func,
                    TO_CHAR(DATA_MARCACAO, 'DD-MM-YYYY') AS data_marc,
                    TO_CHAR(HORA_ENTRADA,  'HH:MI')      AS hora_ent,
                    TO_CHAR(HORA_SAIDA,    'HH:MI')      AS hora_sai
                FROM LABDATABASE.MARCACOES
                WHERE CODIGO_MARCACAO = :1
            """, [id_marc])

            oracle.write("""
                DELETE FROM LABDATABASE.MARCACOES
                 WHERE CODIGO_MARCACAO = :1
            """, [id_marc])

            marc_E = Marcacao(
                id_marc=df.id_marc.values[0],
                id_func=df.id_func.values[0],
                data_marc=df.data_marc.values[0],
                hora_marc=df.hora_ent.values[0],
                tipo="E"
            )
            marc_S = Marcacao(
                id_marc=df.id_marc.values[0],
                id_func=df.id_func.values[0],
                data_marc=df.data_marc.values[0],
                hora_marc=df.hora_sai.values[0],
                tipo="S"
            )

            print("Marcação (período) removida com sucesso!")
            print("  ", marc_E.to_string())
            print("  ", marc_S.to_string())
        else:
            print(f"O id_marc {id_marc} não existe.")

    # --------------------------
    # Verificações de existência
    # --------------------------

    def verifica_existencia_marcacao(self, oracle: OracleQueries, id_marc: int) -> bool:
        """
        True se NÃO existe a marcação (período).
        """
        df = oracle.sqlToDataFrame("""
            SELECT 1 AS existe
              FROM LABDATABASE.MARCACOES
             WHERE CODIGO_MARCACAO = :1
        """, [id_marc])
        return df.empty

    def verifica_existencia_funcionario(self, oracle: OracleQueries, id_func: int) -> bool:
        """
        True se NÃO existe o funcionário.
        """
        df = oracle.sqlToDataFrame("""
            SELECT 1 AS existe
              FROM LABDATABASE.FUNCIONARIOS
             WHERE CODIGO_FUNCIONARIO = :1
        """, [id_func])
        return df.empty
