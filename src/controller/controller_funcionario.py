from conexion.oracle_queries import OracleQueries
from src.model.funcionario import Funcionario

class ControllerFuncionario:
    def __init__(self):
        self.db = OracleQueries()

    def listar(self):
        self.db.connect()
        sql = "SELECT id_func, nome, cpf, cargo FROM funcionario ORDER BY nome"
        return self.db.sqlToDataFrame(sql)

    def buscar_por_cpf(self, cpf: str):
        self.db.connect()
        sql = "SELECT id_func, nome, cpf, cargo FROM funcionario WHERE cpf = :1"
        df = self.db.sqlToDataFrame(sql, [cpf])
        return None if df.empty else df.iloc[0].to_dict()

    def inserir(self, nome: str, cpf: str, cargo: str):
        self.db.connect()
        try:
            funcionario = Funcionario(None, nome, cpf, cargo)
        except ValueError as e:
            raise ValueError(str(e))
        if self.buscar_por_cpf(cpf):
            raise ValueError("Já existe funcionário com esse CPF.")
        sql = """
            INSERT INTO funcionario (id_func, nome, cpf, cargo)
            VALUES (seq_func.NEXTVAL, :1, :2, :3)
        """
        self.db.execute(sql, [nome, cpf, cargo])
        # Retorna o funcionário recém-inserido
        return self.buscar_por_cpf(cpf)

    def atualizar(self, id_func: int, nome: str, cargo: str):
        self.db.connect()
        sql = "UPDATE funcionario SET nome = :1, cargo = :2 WHERE id_func = :3"
        self.db.execute(sql, [nome, cargo, id_func])
        # Retorna o funcionário atualizado
        sql = "SELECT id_func, nome, cpf, cargo FROM funcionario WHERE id_func = :1"
        df = self.db.sqlToDataFrame(sql, [id_func])
        return None if df.empty else df.iloc[0].to_dict()

    def remover(self, id_func: int):
        self.db.connect()
        try:
            self.db.conn.begin()  # Inicia transação (ajuste conforme seu OracleQueries)
            chk = "SELECT COUNT(*) qtd FROM marcacao WHERE id_func = :1"
            qtd = self.db.sqlToDataFrame(chk, [id_func])["QTD"][0]
            if qtd > 0:
                raise ValueError("Funcionário possui marcações; remova/realocar antes de excluir.")
            self.db.execute("DELETE FROM alocacao WHERE id_func = :1", [id_func])
            self.db.execute("DELETE FROM ajuste   WHERE id_func = :1", [id_func])
            self.db.execute("DELETE FROM funcionario WHERE id_func = :1", [id_func])
            self.db.conn.commit()  # Confirma transação
            return True
        except Exception as e:
            self.db.conn.rollback()  # Desfaz alterações em caso de