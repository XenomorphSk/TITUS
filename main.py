#!/usr/bin/python3

# Titus
# version: Beta
# Author: Gabriel Skura Ribeiro

import subprocess, os, pyshark, hashlib, psutil, cpuinfo, random, datetime, magic, pefile, platform, string, bcrypt
import pymysql
from time import sleep
from scapy.all import *
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import Fore, Back, Style, init

init(autoreset=True)

sistema = platform.system()
versao = platform.version()
release = platform.release()
extend_name = platform.platform()

def passwd():
    print('''[+] MODO SENHA SEGURA 
         
         1) Verificação de senha
         2) Guardar senha
         3) Verificar senha armazenada
    ''')
    try:
        c = int(input('Escolha a opção pelo número: '))

        if c == 1:
            senha = input('Digite a sua senha: ')
            chars = list(senha)

            especiais = ['!', '@', '#', '$', '%', '¨', '&', '*']
            numeros = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

            print('Analisando sua senha:', chars)
            sleep(2)

            little = len(chars) < 16
            misto = any(char in especiais for char in chars) and any(char in numeros for char in chars)

            if not little and misto:
                print('[+] Sua senha é forte, está segura... por enquanto...')
            else:
                print('[-] Sua senha é fraca... vou disponibilizar uma melhor:')
                caracteres = string.ascii_letters + string.digits + string.punctuation
                newpass = ''.join(random.choice(caracteres) for _ in range(16))
                print('\n', newpass)

        elif c == 2:
            senha = str(input('Digite a senha que quer guardar: '))
            salt = bcrypt.gensalt()
            hash_senha = bcrypt.hashpw(senha.encode('utf-8'), salt)

            con = pymysql.connect(
                host="localhost",
                user="root",
                password="kali",
                database='titus',
                charset='utf8mb4'
            )

            cursor = con.cursor()
            sql = "INSERT INTO passwords(passhash) VALUES (%s)"
            cursor.execute(sql, (hash_senha.decode('utf-8'),))
            con.commit()

            print(Fore.GREEN + "[+] Senha armazenada com sucesso!")
            cursor.close()
            con.close()

        elif c == 3:
            senha_verificar = input('Digite a senha para verificar: ')
            con = pymysql.connect(
                host="localhost",
                user="root",
                password="kali",
                database='titus',
                charset='utf8mb4'
            )

            cursor = con.cursor()
            cursor.execute("SELECT id, passhash FROM passwords")
            senhas = cursor.fetchall()

            senha_encontrada = False

            for senha in senhas:
                if bcrypt.checkpw(senha_verificar.encode('utf-8'), senha[1].encode() if isinstance(senha[1], str) else senha[1]):
                    print(f"[+] Senha correspondente encontrada! ID: {senha[0]}")
                    senha_encontrada = True
                    break

            if not senha_encontrada:
                print(Fore.RED + "[-] Nenhuma senha correspondente encontrada.")

            cursor.close()
            con.close()

    except ValueError:
        print(Fore.RED + '[-] *ERRO* Entrada inválida! Só é permitido entrada de números!')

def activiti():
    print('\n[+] Monitorando processos ativos... \n')
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent']):
        try:
            info = proc.info
            print(f"PID: {info['pid']} | Processo: {info['name']} | Usuário: {info['username']} | Memória: {info['memory_percent']:.2f}% | CPU: {info['cpu_percent']}%")
        except psutil.NoSuchProcess:
            pass

def calcular_hash(arquivo):
    sha256 = hashlib.sha256()
    try:
        with open(arquivo, 'rb') as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        print(Fore.RED + f"[-] Arquivo {arquivo} não encontrado.")
        return None

def obter_metadados(arquivo):
    try:
        tamanho = os.path.getsize(arquivo)
        mod_time = os.path.getmtime(arquivo)
        mod_time_fmt = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        tipo = magic.from_file(arquivo)
        return {"Tamanho (bytes)": tamanho, "Última modificação": mod_time_fmt, "Tipo": tipo}
    except Exception as e:
        print(Fore.RED + f"[-] Erro ao obter metadados: {e}")
        return None

def main():
    while True:
        print(Fore.CYAN + '''
            1) Análise da Rede
            2) Integridade de Arquivos
            3) Atividade
            4) Senhas 
            5) Sair
        ''')

        try:
            choice = int(input(Fore.YELLOW + 'Escolha um dos módulos através dos números: '))
            if choice == 1:
                network()
            elif choice == 2:
                archives()
            elif choice == 3:
                activiti()
            elif choice == 4:
                passwd()
            elif choice == 5:
                print(Fore.GREEN + "[+] Saindo do programa...")
                break
            else:
                print(Fore.RED + '[-] *ERRO* Opção não conhecida! Tente novamente.')
        except ValueError:
            print(Fore.RED + '[-] *ERRO* Entrada inválida! Só é permitido entrada de números!')
            sleep(2)

if __name__ == "__main__":
    captured_packets = []
    main()
