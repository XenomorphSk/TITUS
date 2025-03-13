#!/bin/bash

# Titus - Script de Instalação
# Autor: Gabriel Skura Ribeiro
# Descrição: Instala todas as dependências necessárias para executar o Titus.

# Atualizando repositórios
echo "[+] Atualizando pacotes..."
sudo apt update && sudo apt upgrade -y

# Instalando pacotes do sistema necessários
echo "[+] Instalando pacotes do sistema..."
sudo apt install -y python3 python3-pip python3-venv \
    tshark clamav clamav-daemon libmagic-dev libmysqlclient-dev

# Atualizando banco de assinaturas do ClamAV
echo "[+] Atualizando ClamAV..."
sudo freshclam

# Instalando servidor MySQL
echo "[+] Instalando servidor MySQL..."
sudo apt install -y mariadb-server
sudo systemctl start mariadb
sudo systemctl enable mariadb

# Criando banco de dados e tabela para o Titus
mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS titus;
USE titus;
CREATE TABLE IF NOT EXISTS passwords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    passhash VARCHAR(100) NOT NULL
);
EOF

# Criando ambiente virtual para o Python
echo "[+] Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalando dependências do Python
echo "[+] Instalando bibliotecas Python..."
pip install --upgrade pip
pip install scapy pyshark hashlib psutil cpuinfo random2 datetime python-magic pefile platform watchdog colorama pymysql bcrypt

# Configurando permissões para captura de pacotes
if [[ $(id -u) -ne 0 ]]; then
    echo "[!] Permissões administrativas são necessárias para capturar pacotes. Execute com sudo."
else
    echo "[+] Ajustando permissões do Python para captura de pacotes..."
    sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)
fi

# Finalização
echo "[+] Instalação concluída. Para rodar o Titus, ative o ambiente virtual:"
echo "source venv/bin/activate"
