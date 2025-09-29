from conexion.oracle_queries import OracleQueries
from src.model.marcacao import Marcacao  

from datetime import datetime

DATE_FMT_DB_IN  = "DD-MM-YYYY"  
DATE_FMT_DB_OUT = "DD-MM-YYYY"  
TIME_FMT_DB     = "HH24:MI"

class ControllerMarcacao:
    def __init__(self):
        self.db = OracleQueries()

    def listar(self, ano_mes: str | None = None):
        """
        ano_mes: string 'YYYY-MM' (ex.: '2025-09') para filtrar por mês.
        A saída data_marc vem como 'DD-MM-YYYY'.
        """
        self.db.connect()
        if ano_mes:
            sql = f"""
                SELECT m.id_marc, m.id_func, f.nome,
                       TO_CHAR(m.data_marc,'{DATE_FMT_DB_OUT}') AS data_marc,
                       TO_CHAR(m.hora_marc,'{TIME_FMT_DB}')      AS hora_marc,
                       m.tipo
                  FROM marcacao m
                  JOIN funcionario f ON f.id_func = m.id_func
                 WHERE TO_CHAR(m.data_marc,'YYYY-MM') = :1
                 ORDER BY m.data_marc, m.id_func, m.tipo
            """
            return self.db.sqlToDataFrame(sql, [ano_mes])
        else:
            sql = f"""
                SELECT m.id_marc, m.id_func, f.nome,
                       TO_CHAR(m.data_marc,'{DATE_FMT_DB_OUT}') AS data_marc,
                       TO_CHAR(m.hora_marc,'{TIME_FMT_DB}')      AS hora_marc,
                       m.tipo
                  FROM marcacao m
                  JOIN funcionario f ON f.id_func = m.id_func
                 ORDER BY m.data_marc DESC, m.id_func, m.tipo
            """
            return self.db.sqlToDataFrame(sql)

    def inserir(self, id_func: int, data_str: str, hora_str: str, tipo: str):
        """
        data_str deve vir em 'DD-MM-YYYY'
        hora_str deve vir em 'HH:MM'
        tipo em 'E' ou 'S'
        """
        self.db.connect()
        tipo_norm = tipo.upper().strip()
    
        try:
            datetime.strptime(data_str, "%d-%m-%Y")
            datetime.strptime(hora_str, "%H:%M")
        except ValueError:
            raise ValueError("Data ou hora em formato inválido. Use DD-MM-YYYY e HH:MM.")
    
        try:
            marcacao = Marcacao(None, id_func, data_str, hora_str, tipo_norm)
        except ValueError as e:
            raise ValueError(str(e))
     
        sql_chk = f"""
            SELECT COUNT(*) qtd
              FROM marcacao
             WHERE id_func = :1
               AND data_marc = TO_DATE(:2,'{DATE_FMT_DB_IN}')
               AND tipo = :3
        """
        qtd = self.db.sqlToDataFrame(sql_chk, [id_func, data_str, tipo_norm])["QTD"][0]
        if qtd > 0:
            raise ValueError("Já existe marcação desse tipo para a data informada.")

        if tipo_norm == "S":
            sql_e = f"""
                SELECT MIN(hora_marc) entrada
                  FROM marcacao
                 WHERE id_func = :1
                   AND data_marc = TO_DATE(:2,'{DATE_FMT_DB_IN}')
                   AND tipo = 'E'
            """
            df_e = self.db.sqlToDataFrame(sql_e, [id_func, data_str])
            if df_e.empty or df_e["ENTRADA"][0] is None:
                raise ValueError("Não é possível registrar saída sem uma entrada no mesmo dia.")

        sql_ins = f"""
            INSERT INTO marcacao (id_marc, id_func, data_marc, hora_marc, tipo)
            VALUES (seq_marc.NEXTVAL, :1,
                    TO_DATE(:2,'{DATE_FMT_DB_IN}'),
                    TO_DATE(:3,'{TIME_FMT_DB}'),
                    :4)
        """
        self.db.execute(sql_ins, [id_func, data_str, hora_str, tipo_norm])

        sql_last = f"""
            SELECT m.id_marc, m.id_func, f.nome,
                   TO_CHAR(m.data_marc,'{DATE_FMT_DB_OUT}') AS data_marc,
                   TO_CHAR(m.hora_marc,'{TIME_FMT_DB}')      AS hora_marc,
                   m.tipo
              FROM marcacao m
              JOIN funcionario f ON f.id_func = m.id_func
             WHERE m.id_func = :1
               AND m.data_marc = TO_DATE(:2,'{DATE_FMT_DB_IN}')
               AND m.hora_marc = TO_DATE(:3,'{TIME_FMT_DB}')
               AND m.tipo = :4
             ORDER BY m.id_marc DESC
        """
        df_last = self.db.sqlToDataFrame(sql_last, [id_func, data_str, hora_str, tipo_norm])
        return None if df_last.empty else df_last.iloc[0].to_dict()

    def remover(self, id_marc: int):
        self.db.connect()

        sql_get = """
            SELECT * FROM marcacao WHERE id_marc = :1
        """
        df = self.db.sqlToDataFrame(sql_get, [id_marc])
        self.db.execute("DELETE FROM marcacao WHERE id_marc = :1", [id_marc])
        return None if df.empty else df.iloc[0].to_dict()