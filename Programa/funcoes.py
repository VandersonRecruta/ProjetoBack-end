import mysql.connector
import random

# Conectando ao banco de dados
conexao = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='bank',
    database='Tryhackme',
)
cursor = conexao.cursor()


# Função para exibir cabeçalho
def Cabecalho(msg):
    """
    Exibe um cabeçalho formatado com o texto fornecido.

    Args:
    msg (str): Mensagem do cabeçalho.
    """
    texto = msg.upper() 
    tam = len(texto)
    print('==' * tam)
    print(f'  {texto}  ')
    print('==' * tam)

# Função para gerar senhas fortes
def gerador_senha():
    """
    Gera senhas fortes.

    Returns:
    list: Lista contendo senhas geradas.
    """
    alfabeto = ['a','b','c','ç','d','e','f','g','h','i','j','k','l','m',
            'n','o','p','q','r','s','t', 'u','v','w','x','y','z']
    numeros = ['0','1','2','3','4','5','6','7','8','9']
    caracteres_especiais = ['#', '!', '@', '$','%','&','*','+']
    senhas = []

    for _ in range(2):
        senha = ''
        senha += random.choice(alfabeto).upper()
        senha += random.choice(numeros)
        senha += random.choice(alfabeto)
        senha += random.choice(caracteres_especiais)
        senhas.append(senha)
    return senhas 

# Função para validar entrada de 'S' ou 'N'
def Entrada(text):
    """
    Valida entrada de 'S' ou 'N'.

    Args:
    text (str): Texto de entrada.

    Returns:
    str: 'S' ou 'N' validados.
    """
    msg = text.upper()
    while True:
        if msg == 'S' or msg == 'N':
            return msg 
        else:
            print('\033[31mErro!\033[m')
            msg = str(input('Digite apenas "S" ou "N":')).upper().strip()

# Função para validar entrada de inteiros
def leiaInt(msg):
    """
    Valida entrada de inteiros.

    Args:
    msg (str): Mensagem para entrada.

    Returns:
    int: Valor inteiro fornecido.
    """
    ok = False
    valor = 0 
    while True:
        n = str(input(msg)).strip()
        if n.isnumeric() and n in '1, 2, 3, 4, 5':
            valor = int(n)
            ok = True
        else:
            print('\033[0;31m Erro! Opção inválida\033[m')
        if ok:
            break
    return valor 

# Função para validar e-mail
def VerificaEmail(msg):
    """
    Valida o formato do e-mail.

    Args:
    msg (str): E-mail a ser verificado.

    Returns:
    str: E-mail validado.
    """
    email = msg.strip()
    while True:
        if email[-10:] == '@gmail.com' or email[-12:] == '@hotmail.com':
            return email
        else:
            print('\033[31mErro! seu e-mail dever conter "@gmail.com"\033[m')
            email = input('Digite seu e-mail:').strip()

# Função para validar senha
def VerificaSenha(msg):
    """
    Valida a senha de acordo com critérios específicos.

    Args:
    msg (str): Senha a ser verificada.

    Returns:
    str: Senha validada.
    """
    senha = msg.strip()
    while True:
        if 8 <= len(senha) <= 10:
            return senha 
        else:
            print('\033[31mSenha Fraca! Sua senha deve conter de 8 a 10 caracteres\033[m')
            senha = input('Digite sua senha:').strip()

# Função para validar dados de e-mail ou senha
def ValidarDados(msg):
    """
    Valida entrada de 'EMAIL' ou 'SENHA'.

    Args:
    msg (str): Mensagem de entrada.

    Returns:
    str: 'EMAIL' ou 'SENHA' validados.
    """
    dado = msg.upper().strip()
    email = 'EMAIL'
    senha = 'SENHA'
    
    if dado == email:
        return 'EMAIL'
    elif dado == senha:
        return 'SENHA'
    else:
        while True:
            print('\033[31mErro! Digite email ou senha!\033[m')
            dado = input('Deseja atualizar e-mail ou senha?').upper().strip()
            if dado == email or dado == senha:
                return dado 
            else:
                continue

# Função para criar registro no banco de dados
def Criar(email, senha):
    """
    Cria um novo registro no banco de dados.

    Args:
    email (str): E-mail para cadastro.
    senha (str): Senha para cadastro.
    """
    CadastrarEmail = email
    CadastrarSenha = senha 
    comando = f'INSERT INTO cadastros(email, senha) VALUES (%s, %s)' 
    cursor.execute(comando, (CadastrarEmail, CadastrarSenha))
    conexao.commit()

# Função para ler dados do banco de dados
def LerDB(email=None, senha=None):
    """
    Lê dados do banco de dados com base no e-mail ou senha fornecidos.

    Args:
    email (str, optional): E-mail a ser pesquisado. Defaults to None.
    senha (str, optional): Senha a ser pesquisada. Defaults to None.

    Returns:
    list: Resultados da busca no banco de dados.
    """
    comando = 'SELECT * FROM cadastros WHERE '
    params = []

    if email and senha:
        comando += 'email = %s and senha = %s'
        params = (email, senha)
    elif email:
        comando += 'email = %s'
        params = (email,)
    elif senha:
        comando += 'senha = %s'
        params = (senha,)
    else:
        return None
    
    try:
        cursor.execute(comando, params)
        resultado = cursor.fetchall()
        return resultado
    except Exception as e:
        print(f'Ocorreu um erro: {e}')
        return None

# Função para atualizar dados no banco de dados
def Atualizacao(email, senha, ref):
    """
    Atualiza registros no banco de dados.

    Args:
    email (str): E-mail para atualização.
    senha (str): Senha para atualização.
    ref (str): Referência para atualização (NovoEmail ou NovaSenha).

    Returns:
    bool: True se a atualização foi bem-sucedida, False caso contrário.
    """
    comando = f'UPDATE cadastros SET '
    params = []

    if ref == 'NovoEmail':
        comando += 'email = %s WHERE senha = %s'
        params = (email, senha)
    elif ref == 'NovaSenha':
        comando += 'senha = %s WHERE email = %s'
        params = (senha, email)
    try:
        cursor.execute(comando, params)
        conexao.commit()
        return True
    except Exception as e:
        print(f'Ocorreu um erro: {e}')
        conexao.rollback()
        return False

# Função para deletar registro do banco de dados
def Deletar(email, senha):
    """
    Deleta um registro do banco de dados.

    Args:
    email (str): E-mail do registro a ser deletado.
    senha (str): Senha do registro a ser deletado.
    """
    DeletarEmail = email 
    DeletarSenha = senha 
    comando = f'DELETE FROM cadastros WHERE email = %s and senha = %s'
    cursor.execute(comando, (DeletarEmail, DeletarSenha))
    conexao.commit()
