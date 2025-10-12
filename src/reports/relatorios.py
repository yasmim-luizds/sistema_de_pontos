from conexion.oracle_queries import OracleQueries
class Relatorio:
    def __init__(self):
        with open("sql/relatorio_funcionarios.sql") as f:
            self.query_relatorio_funcionarios = f.read()
        with open("sql/relatorio_marcacoes.sql") as f:
            self.query_relatorio_marcacao = f.read()
        with open("sql/relatorio_marcacoes_funcionarios.sql") as f:
            self.query_relatorio_pontos_funcionarios = f.read()

    def get_relatorio_funcionarios(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_funcionarios))
        input("Pressione Enter para Sair do Relatório de Funcionários")

    def get_relatorio_marcacao(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_marcacao))
        input("Pressione Enter para Sair do Relatório de Marcações de Ponto")

    def get_relatorio_pontos_funcionarios(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_pontos_funcionarios))
        input("Pressione Enter para Sair do Relatório de Marcações por Funcionário")
