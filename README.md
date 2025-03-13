# Titus - Sistema de Análise e Monitoramento

**Versão:** Beta  
**Autor:** Gabriel Skura Ribeiro


![Titus Logo](https://preview.redd.it/lgzzwzkfym481.jpg?width=640&crop=smart&auto=webp&s=5d00cd6bfe00f583fff7acbbeff7e977f7ce09e3)



---

## 🔧 Sobre o Titus

Titus é uma ferramenta de segurança que oferece funcionalidades de:
- **Análise de Rede:** Captura e registro de pacotes de rede.
- **Integridade de Arquivos:** Verifica a integridade de arquivos e escaneia em busca de malwares.
- **Monitoramento de Atividade:** Monitora processos, uso de CPU e memória.
- **Gestão de Senhas:** Armazena senhas de forma segura com hash e verificação.

---

## 🔹 Requisitos do Sistema
- Linux (Debian-based)
- Python 3
- MySQL/MariaDB

---

## ⚖️ Instalação

### 1. Execute o Script de Instalação

```bash
chmod +x install.sh
sudo ./install.sh
```

### 2. Ative o Ambiente Virtual

```bash
source venv/bin/activate
```

---

## ⚡ Uso

Para iniciar o Titus:

```bash
python3 main.py
```

O menu principal será exibido:

```
1) Análise da Rede
2) Integridade de Arquivos
3) Atividade
4) Senhas
5) Sair
```

### Funcionalidades:

- **1) Análise da Rede:** Captura pacotes de rede em tempo real e salva em arquivos `.pcap`.
- **2) Integridade de Arquivos:**
  - Calcula o hash SHA-256 de um arquivo.
  - Realiza verificação de integridade.
  - Escaneia arquivos usando ClamAV.
- **3) Atividade:**
  - Exibe processos ativos e o consumo de recursos.
  - Monitora CPU e memória em tempo real.
- **4) Senhas:**
  - **Verificação:** Avalia a força de uma senha.
  - **Guardar:** Armazena senhas no banco de dados usando bcrypt.
  - **Verificar:** Verifica se uma senha já está armazenada.

---

## 📁 Banco de Dados

Durante a instalação, o banco de dados `titus` é criado com a tabela `passwords`:

```sql
CREATE DATABASE titus;
USE titus;
CREATE TABLE passwords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    passhash VARCHAR(100) NOT NULL
);
```

---

## ❓ Problemas Comuns

- **Permissão de Captura:**
  Se ocorrer erro de permissão para captura de pacotes, execute:
  ```bash
  sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)
  ```

- **Erro ao Conectar com o Banco:**
  Verifique se o MariaDB está rodando:
  ```bash
  sudo systemctl start mariadb
  sudo systemctl enable mariadb
  ```

---

## 🔄 Atualizações Futuras
- Adição de logs detalhados para auditoria.
- Expansão das funções de análise de arquivos.
- Integração com outras ferramentas de segurança.

---

## 🔧 Contribuição
Sugestões e melhorias são bem-vindas!

---

## ⚖️ Licença
Este projeto está licenciado sob a Licença MIT.

