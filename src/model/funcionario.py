import re

class Funcionario:
    def __init__(self, id_func, nome, cpf, cargo):
        self.__id_func = id_func
        self.__nome = nome
        self.set_cpf(cpf)  # Validação ao criar
        self.__cargo = cargo

    # Função de validação de CPF
    def validar_cpf(self, cpf: str) -> bool:
        cpf = re.sub(r'[^0-9]', '', cpf)
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        for i in range(9, 11):
            soma = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i))
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

    def to_string(self):
        return f"[{self.__id_func}] {self.__nome} • CPF: {self.__cpf} • Cargo: {self.__cargo}"

    def __str__(self):
        return