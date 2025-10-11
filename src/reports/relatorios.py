from conexion.oracle_queries import OracleQueries

class Relatorio:
    def __init__(self):
        with open("sql/relatorio_funcionarios.sql") as f:
            self.query_relatorio_funcionarios = f.read()

        with open("sql/relatorio_marcacoes.sql") as f:
            self.query_relatorio_marcacoes = f.read()

        with open("sql/relatorio_marcacoes_funcionarios.sql") as f:
            self.query_relatorio_marcacoes_funcionarios = f.read()

    def get_relatorio_funcionarios(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_funcionarios))
        input("Pressione Enter para Sair do Relatório de Funcionários")

    def get_relatorio_marcacoes(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_marcacoes))
        input("Pressione Enter para Sair do Relatório de Marcações de ponto")

    def get_relatorio_marcacoes_funcionarios(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_marcacoes_funcionarios))
        input("Pressione Enter para Sair do Relatório de Marcações de ponto por Funcionários")
