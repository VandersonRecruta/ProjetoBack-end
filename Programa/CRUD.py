import mysql.connector
from funcoes import Criar, LerDB, Atualizacao , Deletar, Cabecalho, VerificaEmail, VerificaSenha, leiaInt,Entrada, gerador_senha, ValidarDados 

# Conectando ao banco de dados
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin',
    database='Usuarios',
)
cursor = conexao.cursor()


try:
    while True:
        # Exibe o cabeçalho do sistema
        Cabecalho('SISTEMA')
        print('-' * 30)
        # Mostra as opções disponíveis para o usuário
        print('''    [1] Login
    [2] Cadastro
    [3] Atualizar Cadastro
    [4] Deletar Conta
    [5] Sair do programa  ''')
        print('-' * 30)
        # Pede ao usuário para escolher uma opção
        opcao = leiaInt('Opção:')

        if opcao == 1:
            # Opção de login
            Cabecalho('login')
            # Solicita o e-mail e a senha
            email = VerificaEmail(input('Digite seu E-mail:'))
            senha = VerificaSenha(input('Digite sua senha:'))
            # Verifica se as credenciais são válidas no banco de dados
            resultado = LerDB(email, senha)

            if not resultado:
                # Se as credenciais não são válidas, oferece opção de cadastro
                print('\033[31mEmail ou senhas estão incorretos ou Não está cadastrado!\033[m')
                resp = Entrada(input('Deseja se cadastrar?[S/N]:')).upper().strip()
                if resp == 'S':
                    # Inicia o processo de cadastro
                    Cabecalho('cadastro')
                    emailCad = VerificaEmail(input('Digite seu e-mail:'))
                    resp = Entrada(input('Deseja sugerir senha forte?[S/N]:')).upper().strip()
                    if resp == 'S':
                        # Se o usuário deseja uma senha forte, gera uma sugestão
                        senha = gerador_senha()
                        forte = ''
                        for sugestao in senha:
                            forte += sugestao
                        print(f'Sua nova senha é: {forte}', end='') # Sugestão de senha que será mostrada 
                    senha1 = VerificaSenha(input('\nDigite sua senha:'))
                    senhaCad = str(input('Repita sua senha:'))
                    while True:
                        if senha1 == senhaCad:
                            # Se as senhas correspondem, cria o cadastro
                            Criar(emailCad, senhaCad)
                            print('\033[32mCadastro realizado com sucesso!\033[m')
                        else:
                            print('\033[31mSenha incorreta!\033[m')
                            senhaCad = str(input('Repita sua senha:')).strip()
                else:
                    continue
            else:
                print('\033[36mLogin bem sucedido!\033[m')
        elif opcao == 2:
            # Opção de cadastro
            Cabecalho('cadastro')
            emailCad = VerificaEmail(input('Digite seu e-mail:'))
            resp = Entrada(input('Deseja sugerir senha forte?[S/N]')).upper().strip()[0]
            if resp == 'S':
                senha = gerador_senha()
                forte = ''
                for sugestao in senha:
                    forte += sugestao
                print(f'Sua nova senha é: {forte}', end='') # Sugestão de senha que será mostrada 
            senha1 = VerificaSenha(input('\nDigite sua senha:'))
            senhaCad = str(input('Repita sua senha:'))
            while True:
                if senha1 == senhaCad:
                    # Se as senhas correspondem, cria o cadastro
                    Criar(emailCad, senhaCad)
                    print('\033[32mCadastro realizado com sucesso!\033[m')
                else:
                    print('\033[31mSenha incorreta!\033[m')
                    senhaCad = str(input('Repita sua senha:'))
        elif opcao == 3:
            # Opção para atualizar e-mail ou senha
            Cabecalho('Atualizar')
            dado = ValidarDados(input('Deseja atualizar e-mail ou senha?'))
            if dado == 'EMAIL':
                # Atualização de e-mail
                Cabecalho('E-mail Update')
                NovoEmail = VerificaEmail(input('Digite o novo e-mail:'))
                Senha = VerificaSenha(input('Digite sua senha para confirmar:'))
                resultados = LerDB(senha=Senha)
                if not resultados:
                    print('\033[31mSenha incorreta!\033[m')
                else:
                    Nemail = 'NovoEmail'
                    # Realiza a atualização do e-mail no banco de dados
                    ok = Atualizacao(email=NovoEmail, senha=Senha, ref=Nemail)
                    if ok:
                        print('\033[32mEmail atualizado com sucesso!\033[m')
            elif dado == 'SENHA':
                # Atualização de senha
                Cabecalho('Senha Update')
                Email = VerificaEmail(input('Digite seu email:'))
                resp = Entrada(input('Deseja sugerir senha forte?[S/N]:')).upper().strip()
                if resp == 'S':
                    # Gera uma sugestão de senha forte
                    senha = gerador_senha()
                    forte = ''
                    for sugestao in senha:
                        forte += sugestao
                    print(f'Sua nova senha é: {forte}', end='') # Sugestão de senha que será mostrada 
                NovaSenha01 = VerificaSenha(input('\nDigite sua nova senha:'))
                NovaSenha = str(input('Repita sua nova senha:'))
                while True:
                    if NovaSenha01 == NovaSenha:
                        resultados = LerDB(email=Email)
                        if not resultados:
                            print('\033[31mSeu e-mail está incorreto!\033[m')
                            break 
                        else:
                            Nsenha = 'NovaSenha'
                            # Realiza a atualização da senha no banco de dados
                            ok = Atualizacao(email=Email, senha=NovaSenha, ref=Nsenha)
                            if ok:
                                print('\033[32mSenha atualizada com sucesso!\033[m')
                                break 
                    else:
                        print('\033[31mSenha incorreta!\033[m')
                        NovaSenha = str(input('Repita sua senha:')).strip()
        elif opcao == 4:
            # Opção para deletar conta
            Cabecalho('Deletar')
            emailDel = VerificaEmail(input('Digite o e-mail que deseja deletar:'))
            senhaDel = VerificaSenha(input('Digite sua senha para confirmar:'))
            resultado = LerDB(senha=senhaDel)
            if not resultado:
                print('\033[31mSenha incorreta!\033[m')
            else:   
                # Deleta a conta do usuário no banco de dados
                Deletar(emailDel, senhaDel)
                print('\033[33mCadastro deletado!\033[m')
        elif opcao == 5:
            print('\033[35mEncerrando programa...\033[m')
            break 
except Exception as e:
    # Captura qualquer exceção que ocorra durante a execução
    print(f'Ocorreu um erro: {e}')
finally:
    # Encerra a conexão com o banco de dados
    cursor.close()
    conexao.close()
