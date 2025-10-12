from model.marcacao import Marcacao
from conexion.oracle_queries import OracleQueries

class Controller_Marcacao:
    def __init__(self):
        pass

    def inserir_marcacao(self) -> Marcacao | None:
        oracle = OracleQueries()
        cursor = oracle.connect()
        output_value = cursor.var(int)

        id_func = int(input("ID do Funcionário (existente): "))

        # Verifica se o funcionário existe antes de inserir a marcação
        if self.verifica_existencia_funcionario(oracle, id_func):
            print(f"O ID do funcionário {id_func} não existe. Cadastre o funcionário primeiro.")
            return None

        data_marc = input("Data (DD-MM-YYYY): ")
        hora_marc = input("Hora (HH:MM): ")
        tipo = input("Tipo (E/S): ").strip().upper()[:1]

        data = dict(
            novo_id=output_value,
            id_func=id_func,
            data_marc=data_marc,
            hora_marc=hora_marc,
            tipo=tipo
        )

        cursor.execute(
            """
            begin
                :novo_id := MARCACAO_ID_MARC_SEQ.NEXTVAL;
                insert into marcacao (id_marc, id_func, data_marc, hora_marc, tipo)
                values (
                    :novo_id,
                    :id_func,
                    TO_DATE(:data_marc, 'DD-MM-YYYY'),
                    TO_DATE(:hora_marc, 'HH24:MI'),
                    :tipo
                );
            end;
            """,
            data,
        )

        id_marc = output_value.getvalue()
        oracle.conn.commit()

        df = oracle.sqlToDataFrame(
            f"""
            select m.id_marc, m.id_func,
                   TO_CHAR(m.data_marc,'DD-MM-YYYY') as data_marc,
                   TO_CHAR(m.hora_marc,'HH24:MI')    as hora_marc,
                   m.tipo
              from marcacao m
             where m.id_marc = {id_marc}
            """
        )
        nova = Marcacao(
            df.id_marc.values[0],
            df.id_func.values[0],
            df.data_marc.values[0],
            df.hora_marc.values[0],
            df.tipo.values[0],
        )
        print(nova.to_string())
        return nova

    def atualizar_marcacao(self) -> Marcacao | None:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        id_marc = int(input("ID da Marcação que irá alterar: "))

        if not self.verifica_existencia_marcacao(oracle, id_marc):
            nova_data = input("Nova Data (DD-MM-YYYY): ")
            nova_hora = input("Nova Hora (HH:MM): ")
            novo_tipo = input("Novo Tipo (E/S): ").strip().upper()[:1]

            oracle.write(f"""
                update marcacao
                   set data_marc = TO_DATE('{nova_data}','DD-MM-YYYY'),
                       hora_marc = TO_DATE('{nova_hora}','HH24:MI'),
                       tipo      = '{novo_tipo}'
                 where id_marc = {id_marc}
            """)

            df = oracle.sqlToDataFrame(
                f"""
                select id_marc, id_func,
                       TO_CHAR(data_marc,'DD-MM-YYYY') as data_marc,
                       TO_CHAR(hora_marc,'HH24:MI')    as hora_marc,
                       tipo
                  from marcacao
                 where id_marc = {id_marc}
                """
            )
            atualizado = Marcacao(
                df.id_marc.values[0],
                df.id_func.values[0],
                df.data_marc.values[0],
                df.hora_marc.values[0],
                df.tipo.values[0],
            )
            print(atualizado.to_string())
            return atualizado
        else:
            print(f"O ID da marcação {id_marc} não existe.")
            return None

    def excluir_marcacao(self) -> None:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        id_marc = int(input("ID da Marcação que irá excluir: "))

        if not self.verifica_existencia_marcacao(oracle, id_marc):
            df = oracle.sqlToDataFrame(
                f"""
                select id_marc, id_func,
                       TO_CHAR(data_marc,'DD-MM-YYYY') as data_marc,
                       TO_CHAR(hora_marc,'HH24:MI')    as hora_marc,
                       tipo
                  from marcacao
                 where id_marc = {id_marc}
                """
            )
            oracle.write(f"delete from marcacao where id_marc = {id_marc}")
            excluida = Marcacao(
                df.id_marc.values[0],
                df.id_func.values[0],
                df.data_marc.values[0],
                df.hora_marc.values[0],
                df.tipo.values[0],
            )
            print("Marcação removida com sucesso!")
            print(excluida.to_string())
        else:
            print(f"O id_marc {id_marc} não existe.")

    def verifica_existencia_marcacao(self, oracle: OracleQueries, id_marc: int) -> bool:
        df = oracle.sqlToDataFrame(
            f"select id_marc from marcacao where id_marc = {id_marc}"
        )
        # True se não existe
        return df.empty

    def verifica_existencia_funcionario(self, oracle: OracleQueries, id_func: int) -> bool:
        df = oracle.sqlToDataFrame(
            f"select id_func from funcionario where id_func = {id_func}"
        )
        # True se não existe
        return df.empty