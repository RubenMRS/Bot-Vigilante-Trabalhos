# 🤖 Bot Vigilante de Empregos (Net-Empregos)

Um bot de Telegram interativo craido em Python que pesquisa vagas no site **Net-Empregos.com** em tempo real. Ao contrário dos alertas normais, este bot valida o contexto (Título + Localização + Empresa) para garantir que os resultados correspondem exatamente ao que procuras.

## 🚀 Funcionalidades

* **Interativo:** Não precisa de reiniciar. Basta enviar uma mensagem no Telegram (ex: `Python Porto`).
* **Fiscal Rigoroso:** Verifica se as palavras-chave existem realmente no bloco do anúncio (evita "falsos positivos").
* **Anti-Spam:** Limita os resultados a 8 por pesquisa para não poluir o chat.
* **Multi-Plataforma:** Corre em Windows, Linux ou macOS (local ou cloud).

## 🛠️ Pré-requisitos

* Python 3.8 ou superior.
* Uma conta no Telegram.

## 📦 Instalação

1.  **Clona ou baixa este projeto:**
    ```bash
    git clone https://github.com/RubenMRS/Bot-Vigilante-Trabalhos.git
    cd vigilante-empregos
    ```

2.  **Cria um ambiente virtual (Recomendado):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instala as dependências:**
    ```bash
    pip install requests beautifulsoup4
    ```

## ⚙️ Configuração

1.  Abre o ficheiro `vigilante.py`.
2.  Encontra a variável `TOKEN` nas primeiras linhas.
3.  Substitui `"COLA_O_TEU_TOKEN_AQUI"` pelo token que recebeste do **@BotFather** no Telegram.

# Exemplo:
TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
▶️ Como Usar
Inicia o Bot:

Bash

python vigilante.py
No Telegram:

Procura pelo teu bot e clica em Start.

Escreve o que procuras. Exemplos:

Recepcionista

Motorista Lisboa

Python Junior Remoto

O bot irá responder com os links diretos das vagas encontradas.

🛡️ Estrutura do Código
requests: Faz os pedidos HTTP ao site e à API do Telegram.

BeautifulSoup: Faz o parsing do HTML para extrair vagas.

re (Regex): Valida se os links são ofertas reais (IDs numéricos).

urllib: Trata os termos de pesquisa para formato URL.

⚠️ Aviso Legal
Este script foi criado para fins educativos e de automação pessoal. O uso excessivo de web scraping pode bloquear o teu IP temporariamente no site alvo. O script já inclui pausas (time.sleep) para mitigar esse risco.

Assim, quem baixar o teu projeto só precisa de fazer pip install -r requirements.txt.

Autor: Rúben Silva
