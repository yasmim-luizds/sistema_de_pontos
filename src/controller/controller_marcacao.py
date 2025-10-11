from conexion.oracle_queries import OracleQueries
from model.funcionario import Funcionario
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
        if ano_mes: # filtra por mês 
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
            datetime.strptime(data_str, "%d-%m-%Y") # Apenas valida a data e hora
            datetime.strptime(hora_str, "%H:%M") 
        except ValueError:
            raise ValueError("Data ou hora em formato inválido. Use DD-MM-YYYY e HH:MM.")
    
        try:
            marcacao = Marcacao(None, id_func, data_str, hora_str, tipo_norm) # Valida data, hora e tipo
        except ValueError as e:
            raise ValueError(str(e)) 
     
        sql_chk = f"""
            SELECT COUNT(*) qtd
              FROM marcacao
             WHERE id_func = :1
               AND data_marc = TO_DATE(:2,'{DATE_FMT_DB_IN}')
               AND tipo = :3
        """
        qtd = self.db.sqlToDataFrame(sql_chk, [id_func, data_str, tipo_norm])["QTD"][0] # Verifica se já existe marcação do mesmo tipo na mesma data
        if qtd > 0:
            raise ValueError("Já existe marcação desse tipo para a data informada.")

        if tipo_norm == "S": # Se for saída, verifica se há uma entrada no mesmo dia
            sql_e = f"""
                SELECT MIN(hora_marc) entrada
                  FROM marcacao
                 WHERE id_func = :1
                   AND data_marc = TO_DATE(:2,'{DATE_FMT_DB_IN}')
                   AND tipo = 'E'
            """
            df_e = self.db.sqlToDataFrame(sql_e, [id_func, data_str]) # Busca a entrada mais antiga do dia
            if df_e.empty or df_e["ENTRADA"][0] is None: # Se não houver entrada, não permite registrar saída
                raise ValueError("Não é possível registrar saída sem uma entrada no mesmo dia.")

        sql_ins = f"""
            INSERT INTO marcacao (id_marc, id_func, data_marc, hora_marc, tipo)
            VALUES (seq_marc.NEXTVAL, :1,
                    TO_DATE(:2,'{DATE_FMT_DB_IN}'), 
                    TO_DATE(:3,'{TIME_FMT_DB}'),
                    :4)
        """
        self.db.execute(sql_ins, [id_func, data_str, hora_str, tipo_norm]) # Insere a marcação

         # Retorna a marcação recém-inserida

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
        df_last = self.db.sqlToDataFrame(sql_last, [id_func, data_str, hora_str, tipo_norm]) # Busca a marcação recém-inserida
        return None if df_last.empty else df_last.iloc[0].to_dict() # Retorna como dicionário
    
    def atualizar(self, id_marc: int, data_str: str, hora_str: str):
        self.db.connect()

        # Busca a marcação atual para obter o id_func
        sql_get = """
            SELECT m.id_marc, m.id_func,
                TO_CHAR(m.data_marc,'DD-MM-YYYY') AS data_marc,
                TO_CHAR(m.hora_marc,'HH24:MI')    AS hora_marc,
            FROM marcacao m
            WHERE m.id_marc = :1
        """
        df_old = self.db.sqlToDataFrame(sql_get, [id_marc]) # Busca a marcação pelo ID
        if df_old.empty: # Se não encontrar, retorna None
            return None

        id_func_atual = int(df_old.iloc[0]["ID_FUNC"]) # guarda o id_func atual para validações
        tipo_atual = str(df_old.iloc[0]["TIPO"]).strip().upper() # guarda o tipo atual para validações
        

        # 2) Normaliza/valida formatos básicos no Python
        try:
            datetime.strptime(data_str, "%d-%m-%Y") 
            datetime.strptime(hora_str, "%H:%M")
        except ValueError:
            raise ValueError("Data ou hora em formato inválido. Use DD-MM-YYYY e HH:MM.")

        # 3) Validação de domínio via modelo Marcacao (formata e valida tipo)
        try:
            # Usa o modelo para garantir regras (E/S) e normalização de strings
            Marcacao(id_marc, id_func_atual, data_str, hora_str, tipo_atual)
        except ValueError as e:
            raise ValueError(str(e))

        # 4) Impedir duplicidade
        sql_chk_dup = """
            SELECT COUNT(*) qtd
            FROM marcacao
            WHERE id_func   = :1
            AND data_marc = TO_DATE(:2,'DD-MM-YYYY')
            AND tipo      = :3
            AND id_marc  <> :4
        """
        df_dup = self.db.sqlToDataFrame(sql_chk_dup, [id_func_atual, data_str, tipo_atual, id_marc])
        if int(df_dup.iloc[0]["QTD"]) > 0:
            raise ValueError("Já existe marcação desse tipo para a data informada.")

        # 5) Regra de negócio: se for SAÍDA, precisa ter ENTRADA no mesmo dia
        if tipo_atual == "S":
            sql_e = """
                SELECT MIN(hora_marc) entrada
                FROM marcacao
                WHERE id_func   = :1
                AND data_marc = TO_DATE(:2,'DD-MM-YYYY')
                AND tipo = 'E'
            """
            df_e = self.db.sqlToDataFrame(sql_e, [id_func_atual, data_str]) # Busca a entrada mais antiga do dia
            if df_e.empty or df_e.iloc[0]["ENTRADA"] is None:
                raise ValueError("Não é possível registrar saída sem uma entrada no mesmo dia.")


        # 6) Executa o UPDATE com binds e TO_DATE
        sql_upd = """
            UPDATE marcacao
            SET data_marc = TO_DATE(:1,'DD-MM-YYYY'),
                hora_marc = TO_DATE(:2,'HH24:MI'),
            WHERE id_marc   = :4
        """
        self.db.execute(sql_upd, [data_str, hora_str, id_marc])

        # 7) Retorna o registro atualizado com formatação amigável e nome do funcionário
        sql_sel = """
            SELECT m.id_marc, m.id_func, f.nome,
                TO_CHAR(m.data_marc,'DD-MM-YYYY') AS data_marc,
                TO_CHAR(m.hora_marc,'HH24:MI')    AS hora_marc,
                m.tipo
            FROM marcacao m
            JOIN funcionario f ON f.id_func = m.id_func
            WHERE m.id_marc = :1
        """
        df_upd = self.db.sqlToDataFrame(sql_sel, [id_marc])
        return None if df_upd.empty else df_upd.iloc[0].to_dict()


    def remover(self, id_marc: int):
        self.db.connect()

        sql_get = """
            SELECT * FROM marcacao WHERE id_marc = :1
        """
        df = self.db.sqlToDataFrame(sql_get, [id_marc]) # Busca a marcação antes de remover
        self.db.execute("DELETE FROM marcacao WHERE id_marc = :1", [id_marc]) # Remove a marcação
        return None if df.empty else df.iloc[0].to_dict() # Retorna a marcação removida como dicionário