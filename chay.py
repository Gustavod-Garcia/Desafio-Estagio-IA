import ollama
from buscar import encontrar_documentos_relevantes, carregar_dados_e_preparar_busca

# O nome do modelo que baixei no Ollama
MODELO_LLM = 'gemma:2b'

def formatar_prompt(query, contexto):
    """
    Cria o prompt final para o LLM, juntando a busca (contexto)
    e a pergunta do usuário (query).
    """
    prompt = f"""
    Você é um assistente de IA especializado em analisar documentos oficiais (Leis, Portarias, Resoluções).
    Sua tarefa é responder à pergunta do usuário usando APENAS o contexto fornecido.
    Se a resposta não estiver no contexto, diga "A informação não foi encontrada nos documentos fornecidos."

    --- CONTEXTO ---
    {contexto}
    --- FIM DO CONTEXTO ---

    PERGUNTA DO USUÁRIO:
    {query}

    RESPOSTA:
    """
    return prompt

# --- Script Principal ---
if __name__ == "__main__":

    # 1. Prepara o motor de busca (TF-IDF) do arquivo buscar.py
    try:
        carregar_dados_e_preparar_busca()
    except Exception as e:
        print(f"Não foi possível iniciar o motor de busca: {e}")
        exit()

    print("\n--- Chatbot de Documentos (Estágio IA) ---")
    print("Servidor LLM local: Ollama")
    print(f"Modelo LLM: {MODELO_LLM}")
    print("Digite 'sair' para terminar.")

    # 2. Loop do Chat
    while True:
        query = input("\nO que você gostaria de saber? \n> ")

        if query.lower() == 'sair':
            break

        # 3. Buscar documentos relevantes
        print("Buscando documentos relevantes...")
        resultados_busca = encontrar_documentos_relevantes(query, top_n=1)

        if not resultados_busca:
            print("Desculpe, não encontrei nenhum documento relevante para essa pergunta.")
            continue

        # 4. Montar o contexto para o LLM
        contexto_texto_completo = resultados_busca[0]['texto_contexto']
        nome_arquivo_contexto = resultados_busca[0]['nome_arquivo']

        print(f"Usando contexto do arquivo: {nome_arquivo_contexto}...")

        # 5. Gerar a resposta com o LLM
        prompt_final = formatar_prompt(query, contexto_texto_completo)

        try:
            # Chama o Ollama (que deve estar rodando na máquina)
            response = ollama.chat(
                model=MODELO_LLM,
                messages=[{'role': 'user', 'content': prompt_final}],
                stream=True # Resposta vem em "pedaços", como no ChatGPT
            )

            print("\nResposta do Assistente:")
            # Imprime a resposta pedaço por pedaço
            for chunk in response:
                print(chunk['message']['content'], end='', flush=True)
            print("\n") # Pula linha no final

        except Exception as e:
            print(f"\nErro ao comunicar com o Ollama: {e}")
            print("Verifique se o Ollama está instalado e rodando na sua máquina.")
            print("Você pode ter rodado 'ollama pull gemma:2b'?")
            break
