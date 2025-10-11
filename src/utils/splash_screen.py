from conexion.oracle_queries import OracleQueries
from utils import config

class SplashScreen:

    def __init__(self):
        self.qry_total_marcacoes = config.QUERY_COUNT.format(tabela="marcacao")
        self.qry_total_funcionarios = config.QUERY_COUNT.format(tabela="funcionarios")
        self.created_by = "Hellen Karla Costa Campos de Melo, Julia Ogassavara Maia e Yasmim Luiz dos Santos"
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2025/2"

    def get_total_marcacoes(self):
        
        oracle = OracleQueries()
        oracle.connect()
        
        return oracle.sqlToDataFrame(self.qry_total_marcacoes)["total_marcacoes"].values[0]

    def get_total_funcionarios(self):
        
        oracle = OracleQueries()
        oracle.connect()
        
        return oracle.sqlToDataFrame(self.qry_total_funcionarios)["total_funcionarios"].values[0]

    def get_updated_screen(self):
        return f"""
    #################################################################################################################
    #                                          SISTEMA DE CONTROLE DE MARCAÇÕES DE PONTO                                         
    #                                                                                                               
    #  TOTAL DE REGISTROS:                                                                                          
    #      1 - MARCAÇÕES: {str(self.get_total_marcacoes()).rjust(5)}
    #      2 - FUNCIONARIOS: {str(self.get_total_funcionarios()).rjust(5)}
    #                                                                                                               
    #  CRIADO POR: {self.created_by}
    #                                                                                                               
    #  PROFESSOR:  {self.professor}
    #                                                                                                               
    #  DISCIPLINA: {self.disciplina}
    #              {self.semestre}
    #                                                                                                               
    #################################################################################################################
    """
