from datetime import datetime # importa a biblioteca datetime para manipulação de datas e horas

# constantes que definem = DD-MM-YYYY formato usado internamente
DATE_FMT = "%d-%m-%Y"   
TIME_FMT = "%H:%M"

class Marcacao:
    """
    data_marc: 'DD-MM-YYYY'
    hora_marc: 'HH:MM'
    tipo: 'E' (entrada) ou 'S' (saída)
    """
    def __init__(self, id_marc, id_func, data_marc, hora_marc, tipo, nome_func=None): #construtor da classe
        self.__id_marc = id_marc
        self.__id_func = id_func
        self.set_data_marc(data_marc)   # normaliza
        self.set_hora_marc(hora_marc)   # normaliza
        self.set_tipo(tipo)             # valida
        self.__nome_func = nome_func

    # getters
    def get_id_marc(self):  
        return self.__id_marc
    def get_id_func(self):  
        return self.__id_func
    def get_data_marc(self): 
        return self.__data_marc
    def get_hora_marc(self): 
        return self.__hora_marc
    def get_tipo(self):      
        return self.__tipo
    def get_nome_func(self): 
        return self.__nome_func

    # setters
    def set_id_marc(self, id_marc: int): 
        self.__id_marc = id_marc
    def set_id_func(self, id_func: int): 
        self.__id_func = id_func

    def set_data_marc(self, data_marc):
        try:
            self.__data_marc = datetime.strptime(str(data_marc), DATE_FMT).strftime(DATE_FMT) # tenta converter a data para o formato da constante DATE_FMT
        except ValueError:
            raise ValueError("Data inválida. Use o formato DD-MM-YYYY.")

    def set_hora_marc(self, hora_marc):
        try:
            self.__hora_marc = datetime.strptime(str(hora_marc), TIME_FMT).strftime(TIME_FMT) # tenta converter a hora para o formato da constante TIME_FMT
        except ValueError:
            raise ValueError("Hora inválida. Use o formato HH:MM.")

    def set_tipo(self, tipo):
        t = str(tipo).strip().upper() #valida o tipo, convertendo para maiúsculas e removendo espaços em branco
        if t not in {"E", "S"}:
            raise ValueError("Tipo inválido: use 'E' (entrada) ou 'S' (saída).")
        self.__tipo = t #armazena o tipo validado

    def set_nome_func(self, nome_func): 
        self.__nome_func = nome_func


    def __str__(self) -> str:
        nome = self.__nome_func or f"FUNC:{self.__id_func}"
        tipo_txt = "Entrada" if self.__tipo == "E" else "Saída"
        idtxt = self.__id_marc if self.__id_marc is not None else "—"
        return f"[{idtxt}] {nome} • {self.__data_marc} {self.__hora_marc} • {tipo_txt}"

