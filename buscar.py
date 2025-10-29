import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Configuração ---
ARQUIVO_DADOS = "documentos.json"

# --- Variáveis Globais (para não recarregar toda hora) ---
documentos = []
textos = []
vectorizer = TfidfVectorizer()
matriz_tfidf = None

def carregar_dados_e_preparar_busca():
    """
    Carrega o JSON e treina o buscador TF-IDF.
    Isso só precisa ser feito uma vez quando o programa inicia.
    """
    global documentos, textos, vectorizer, matriz_tfidf

    try:
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
            documentos = json.load(f)

        # 1. Pega o texto e o nome de cada documento
        textos = [doc['texto_completo'] for doc in documentos]

        # 2. "Treina" o vetorizador com nossos textos
        print("Preparando motor de busca (TF-IDF)...")
        vectorizer = TfidfVectorizer(
            stop_words=None, # Você pode adicionar stop words em português se quiser
            ngram_range=(1, 2) # Considera palavras sozinhas e pares (ex: "inteligencia", "artificial", "inteligencia artificial")
        )
        matriz_tfidf = vectorizer.fit_transform(textos)
        print("Motor de busca pronto.")

    except FileNotFoundError:
        print(f"Erro: Arquivo '{ARQUIVO_DADOS}' não encontrado.")
        print("Por favor, rode 'python processar.py' primeiro.")
        exit()
    except Exception as e:
        print(f"Erro ao carregar ou processar dados: {e}")
        exit()

def encontrar_documentos_relevantes(query_usuario, top_n=3):
    """
    Objetivo 3: Recebe uma busca e retorna os N documentos mais relevantes.
    """
    if matriz_tfidf is None:
        print("Motor de busca não iniciado. Carregando dados...")
        carregar_dados_e_preparar_busca()

    # 1. Transforma a busca do usuário usando o MESMO vetorizador
    query_tfidf = vectorizer.transform([query_usuario])

    # 2. Calcula a "pontuação" de similaridade
    similaridades = cosine_similarity(query_tfidf, matriz_tfidf).flatten()

    # 3. Pega os índices dos N mais relevantes (em ordem)
    indices_relevantes = similaridades.argsort()[:-top_n-1:-1]

    # 4. Monta a lista de resultados
    resultados = []
    for i in indices_relevantes:
        if similaridades[i] > 0: # Só retorna se tiver alguma relevância
            resultado = {
                "nome_arquivo": documentos[i]['nome_arquivo'],
                "tipo_documento": documentos[i]['tipo_documento'],
                "texto_contexto": documentos[i]['texto_completo'], # Retorna o texto todo
                "pontuacao": similaridades[i]
            }
            resultados.append(resultado)

    return resultados

# --- Teste Rápido ---
# Isso só roda se você executar 'python buscar.py'
if __name__ == "__main__":
    print("--- Teste do Motor de Busca (Objetivo 3) ---")
    carregar_dados_e_preparar_busca()

    # Teste
    resultados_teste = encontrar_documentos_relevantes("Quais os artigos da Lei 9784?")

    if resultados_teste:
        print(f"\nResultados encontrados para a busca:")
        for res in resultados_teste:
            print(f"- {res['nome_arquivo']} (Pontuação: {res['pontuacao']:.4f})")
    else:
        print("Nenhum resultado relevante encontrado.")