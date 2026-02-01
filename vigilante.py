import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
import re
from keep_alive import keep_alive

# --- CONFIGURAÇÕES ---
TOKEN = "8399078278:AAE8UVnwI5f8I6V8mcLtAtIM-TSI8LfO5Ro"

# MUDANÇA: Array vazio, como pediste. Não bloqueia nada.
PALAVRAS_PROIBIDAS = [] 

URL_BASE_TELEGRAM = f"https://api.telegram.org/bot{TOKEN}/"

def enviar_mensagem(chat_id, texto):
    try:
        requests.post(URL_BASE_TELEGRAM + "sendMessage", 
                      data={"chat_id": chat_id, "text": texto, "parse_mode": "HTML"})
    except: pass

def ler_mensagens(offset):
    try:
        url = URL_BASE_TELEGRAM + "getUpdates"
        return requests.get(url, params={"offset": offset, "timeout": 10}).json()
    except: return None

def validar_conteudo(elemento_link, palavras_busca):
    """
    Verifica se as palavras que o user escreveu estão MESMO no anúncio.
    Lê o bloco inteiro (Título + Cidade + Empresa).
    """
    try:
        # Texto completo do bloco do anúncio
        texto_anuncio = elemento_link.parent.text.lower()
        palavras_busca = palavras_busca.lower().split()
        
        match_total = True
        for palavra in palavras_busca:
            # Remove "s" final para "Tradutores" encontrar "Tradutor"
            palavra_limpa = palavra.rstrip('s') 
            
            # Se a palavra tiver mais de 2 letras e não estiver no texto -> Falha
            if len(palavra_limpa) > 2 and palavra_limpa not in texto_anuncio:
                match_total = False
                break
                
        return match_total
    except:
        return False

def pesquisar_no_net_empregos(termo, chat_id):
    enviar_mensagem(chat_id, f"🔎 A filtrar rigorosamente por: <b>{termo}</b>...")
    
    termo_safe = urllib.parse.quote_plus(termo)
    # &categoria=0 garante que procura no site todo
    url_pesquisa = f"https://www.net-empregos.com/pesquisa-empregos.asp?chaves={termo_safe}&categoria=0"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        pagina = requests.get(url_pesquisa, headers=headers)
        soup = BeautifulSoup(pagina.content, 'html.parser')
        todos_links = soup.find_all("a", href=True)
        
        encontrados = 0
        ids_vistos_nesta_ronda = [] 
        
        for link_elem in todos_links:
            if encontrados >= 8: break 
            
            href = link_elem['href']
            titulo = link_elem.text.strip()
            
            # --- FILTROS TÉCNICOS ---
            match = re.search(r'(\d{6,})', href)
            if not match: continue
            if "Ver Oferta" in titulo or len(titulo) < 5: continue
            
            id_vaga = match.group(1)
            if id_vaga in ids_vistos_nesta_ronda: continue

            # --- O FISCAL (Validação Rigorosa) ---
            if not validar_conteudo(link_elem, termo):
                continue

            # --- FILTRO LISTA NEGRA (Agora está vazio, por isso passa tudo) ---
            titulo_lower = titulo.lower()
            if PALAVRAS_PROIBIDAS: # Só verifica se a lista tiver coisas
                if any(p.lower() in titulo_lower for p in PALAVRAS_PROIBIDAS): continue

            # --- SUCESSO ---
            ids_vistos_nesta_ronda.append(id_vaga)
            link_final = href if href.startswith("http") else f"https://www.net-empregos.com{href}"
            
            enviar_mensagem(chat_id, f"🎯 <b>{titulo}</b>\n🔗 {link_final}")
            encontrados += 1
            time.sleep(0.5)

        if encontrados == 0:
            enviar_mensagem(chat_id, "🧹 Não encontrei nenhuma vaga que tenha EXATAMENTE essas palavras todas.")
        else:
            enviar_mensagem(chat_id, f"✅ Encontrei {encontrados} vagas.")

    except Exception as e:
        enviar_mensagem(chat_id, f"❌ Erro: {str(e)}")

def main():
    print("🤖 Bot Iniciado...")
    keep_alive()
    ultimo_update_id = None
    while True:
        updates = ler_mensagens(ultimo_update_id)
        if updates and "result" in updates:
            for item in updates["result"]:
                ultimo_update_id = item["update_id"] + 1
                if "message" in item and "text" in item["message"]:
                    chat_id = item["message"]["chat"]["id"]
                    texto = item["message"]["text"]
                    
                    print(f"📩 Pedido: {texto}")

                    if texto == "/start":
                        enviar_mensagem(chat_id, "Estou pronto. Diz-me o que procuras.")
                    else:
                        pesquisar_no_net_empregos(texto, chat_id)
        time.sleep(1)

if __name__ == "__main__":
    main()