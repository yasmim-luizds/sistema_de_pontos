import re # Importa o módulo de expressões regulares para validação de CPF, aqui ele está sendo usado para limpar o CPF de caracteres não numéricos.

# Define a classe Funcionario com atributos e métodos para manipulação de dados de funcionários.
class Funcionario:
    def __init__(self, id_func, nome, cpf, cargo): #construtor da classe
        self.__id_func = id_func
        self.__nome = nome
        self.set_cpf(cpf)  # Validação ao criar
        self.__cargo = cargo
        #self se trata do objeto instanciado da classe

    # Função de validação de CPF
    def validar_cpf(self, cpf: str) -> bool:
        cpf = re.sub(r'[^0-9]', '', cpf) # Remove caracteres não numéricos
        if len(cpf) != 11 or cpf == cpf[0] * 11: # Verifica se o CPF tem 11 dígitos e não é uma sequência de números iguais
            return False
        for i in range(9, 11):
            soma = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i)) # calcula o dígito verificador (ultimos dois dígitos do CPF) para garantir que o CPF é válido
            digito = ((soma * 10) % 11) % 10
            if int(cpf[i]) != digito:
                return False
        return True

    # getters
    def get_id_func(self): 
        return self.__id_func
    def get_nome(self):    
        return self.__nome
    def get_cpf(self):     
        return self.__cpf
    def get_cargo(self):   
        return self.__cargo

    # setters
    def set_id_func(self, id_func: int): 
        self.__id_func = id_func
    def set_nome(self, nome: str):    
        self.__nome = nome
    def set_cpf(self, cpf: str):     
        if not self.validar_cpf(cpf):
            raise ValueError("CPF inválido.")
        self.__cpf = cpf
    def set_cargo(self, cargo: str):   
        self.__cargo = cargo

    def __str__(self):
        return f"[{self.__id_func}] {self.__nome} • CPF: {self.__cpf} • Cargo: {self.__cargo}"
