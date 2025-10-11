from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_funcionario import ControllerFuncionario
from controller.controller_marcacao import ControllerMarcacao

tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_funcionario = ControllerFuncionario()
ctrl_marcacao = ControllerMarcacao()

def reports(opcao_relatorio: int = 0):
    if opcao_relatorio == 1:
        relatorio.get_relatorio_pontos_funcionarios()
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_marcacao()
    elif opcao_relatorio == 3:
        relatorio.get_relatorio_funcionarios()
    elif opcao_relatorio == 0:
        print(config.MENU_PRINCIPAL)
    else:
        print("Opção inválida. Insira uma opção válida.")

def inserir(opcao_inserir: int = 0):
    try:
        if opcao_inserir == 1:
            # marcar ponto
            id_func  = int(input("ID do funcionário: ").strip()) 
            data_str = input("Data (DD-MM-YYYY): ").strip() 
            hora_str = input("Hora (HH:MM): ").strip() 
            tipo     = input("Tipo (E/S): ").strip()    
            registro = ctrl_marcacao.inserir(id_func, data_str, hora_str, tipo) 
            print("Marcação inserida:", registro)
        elif opcao_inserir == 2:
            # cadastrar funcionário
            nome  = input("Nome: ").strip()  
            cpf   = input("CPF: ").strip()  
            cargo = input("Cargo: ").strip()  
            registro = ctrl_funcionario.inserir(nome, cpf, cargo)
            print("Funcionário inserido:", registro) 
        elif opcao_inserir == 0:
            print(config.MENU_PRINCIPAL) 
        else:
            print("Opção inválida. Insira uma opção válida.")
    except ValueError as e:
        print(f"Erro: {e}")

def atualizar(opcao_atualizar: int = 0):
    try:
        if opcao_atualizar == 1:
            # Atualizar marcação
            id_marc   = int(input("ID da marcação a atualizar: ").strip())
            id_func_atual = int(input("ID do funcionário: ").strip()) 
            data_str  = input("Nova data (DD-MM-YYYY): ").strip() 
            hora_str  = input("Nova hora (HH:MM): ").strip() 
            registro = ctrl_marcacao.atualizar(id_marc, id_func_atual, data_str, hora_str)
            if registro:
                print("Marcação atualizada:", registro)
            else:
                print("Marcação não encontrada.")
        elif opcao_atualizar == 2:
            relatorio.get_relatorio_funcionarios()
            id_func = int(input("ID do funcionário a atualizar: ").strip())
            nome    = input("Novo nome: ").strip()
            cargo   = input("Novo cargo: ").strip()
            registro = ctrl_funcionario.atualizar(id_func, nome, cargo)
            if registro:
                print("Funcionário atualizado:", registro)
            else:
                print("Funcionário não encontrado.")
        elif opcao_atualizar == 0:
            print(config.MENU_PRINCIPAL)
        else:
            print("Opção inválida. Insira uma opção válida.")
    except ValueError as e:
        print(f"Erro: {e}")

def excluir(opcao_excluir: int = 0):
    try:
        if opcao_excluir == 1:
            # Excluir marcação
            id_marc = int(input("ID da marcação a excluir: ").strip())
            apagada = ctrl_marcacao.remover(id_marc)
            if apagada:
                print("Marcação removida:", apagada)
            else:
                print("Marcação não encontrada.")
        elif opcao_excluir == 2:
            # Excluir funcionário
            relatorio.get_relatorio_funcionarios()
            id_func = int(input("ID do funcionário a excluir: ").strip())
            ok = ctrl_funcionario.remover(id_func)
            if ok:
                print("Funcionário removido com sucesso.")
            else:
                print("Funcionário não encontrado ou não removido.")
        elif opcao_excluir == 0:
            print(config.MENU_PRINCIPAL)
        else:
            print("Opção inválida. Insira uma opção válida.")
    except ValueError as e:
        print(f"Erro: {e}")

def run():
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        try:
            opcao = int(input("Escolha uma opção entre 1 e 5: "))
            config.clear_console(1)

            if opcao == 1:
                print(config.MENU_RELATORIOS)
                try:
                    opcao_relatorio = int(input("Escolha uma opção entre 0 e 3: "))
                    config.clear_console(1)
                    reports(opcao_relatorio)
                    config.clear_console(1)
                except ValueError:
                    print("Entrada inválida. Insira um valor inteiro.")
                    config.clear_console(1)

            elif opcao == 2:  # Inserir
                while True:
                    print(config.MENU_ENTIDADES)
                    try:
                        opcao_inserir = int(input("Escolha uma opção entre 0 e 2: "))
                        config.clear_console(1)
                        if opcao_inserir == 0:
                            break
                        inserir(opcao_inserir=opcao_inserir)
                        config.clear_console(1)
                        cont = input("Deseja inserir outro registro? (S/N): ").strip().upper()
                        if cont != 'S':
                            break
                    except ValueError:
                        print("Entrada inválida. Insira um valor inteiro.")
                        config.clear_console(1)

            elif opcao == 3:  # Atualizar
                while True:
                    print(config.MENU_ENTIDADES)
                    try:
                        opcao_atualizar = int(input("Escolha uma opção entre 0 e 2: "))
                        config.clear_console(1)
                        if opcao_atualizar == 0:
                            break
                        atualizar(opcao_atualizar=opcao_atualizar)
                        config.clear_console(1)
                        cont = input("Deseja atualizar outro registro? (S/N): ").strip().upper()
                        if cont != 'S':
                            break
                    except ValueError:
                        print("Entrada inválida. Insira um valor inteiro.")
                        config.clear_console(1)

            elif opcao == 4:  # Remover
                while True:
                    print(config.MENU_ENTIDADES)
                    try:
                        opcao_excluir = int(input("Escolha uma opção entre 0 e 2: "))
                        config.clear_console(1)
                        if opcao_excluir == 0:
                            break
                        excluir(opcao_excluir=opcao_excluir)
                        config.clear_console()
                        print(tela_inicial.get_updated_screen())
                        config.clear_console(1)
                        cont = input("Deseja remover outro registro? (S/N): ").strip().upper()
                        if cont != 'S':
                            break
                    except ValueError:
                        print("Entrada inválida. Insira um valor inteiro.")
                        config.clear_console(1)

            elif opcao == 5:
                print(tela_inicial.get_updated_screen())
                config.clear_console()
                print("Saindo do sistema...")
                exit(0)

            else:
                print("Opção inválida. Insira uma opção válida.")
                config.clear_console(1)

        except ValueError:
            print("Entrada inválida. Insira um valor inteiro.")
            config.clear_console(1)

if __name__ == "__main__":
    run()
