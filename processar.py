# Importa as bibliotecas que vamos usar
import fitz  # Esta é a biblioteca PyMuPDF
import os    # Para interagir com o sistema (encontrar arquivos)
import json  # Para criar o arquivo JSON

# --- Configuração ---
PASTA_DADOS = "dados"  # O nome da pasta onde estão seus PDFs
ARQUIVO_SAIDA = "documentos.json" # O nome do arquivo que vamos criar

def extrair_texto_pdf(caminho_pdf):
    """
    Objetivo 1: Abre um PDF e extrai todo o texto dele.
    """
    try:
        doc = fitz.open(caminho_pdf)  # Abre o arquivo
        texto_completo = ""
        for pagina in doc:  # Passa por cada página
            texto_completo += pagina.get_text() # Adiciona o texto da página
        doc.close()
        return texto_completo
    except Exception as e:
        print(f"Erro ao ler o arquivo {caminho_pdf}: {e}")
        return "" # Retorna vazio se der erro

def classificar_documento(nome_arquivo):
    """
    Objetivo 2: Classifica o documento baseado no nome do arquivo.
    Esta é uma lógica simples que atende ao requisito.
    """
    nome_normalizado = nome_arquivo.lower() # Deixa tudo minúsculo
    
    if nome_normalizado.startswith("lei_"):
        return "Lei"
    if nome_normalizado.startswith("portaria_"):
        return "Portaria"
    if nome_normalizado.startswith("resolucao_"):
        return "Resolução"
    
    return "Outro" # Categoria padrão

# --- Script Principal ---
# Isso só roda quando você executa 'python processar.py'
if __name__ == "__main__":
    
    base_de_dados = [] # Uma lista vazia para guardar nossos dados
    
    print(f"Iniciando processamento da pasta '{PASTA_DADOS}'...")

    # Loop por cada arquivo dentro da pasta PASTA_DADOS
    for nome_arquivo in os.listdir(PASTA_DADOS):
        
        # Só processa arquivos que terminam com .pdf
        if nome_arquivo.endswith(".pdf"):
            
            caminho_completo = os.path.join(PASTA_DADOS, nome_arquivo)
            print(f"Processando: {nome_arquivo}...")
            
            # --- Objetivo 1 ---
            texto = extrair_texto_pdf(caminho_completo)
            
            # --- Objetivo 2 ---
            tipo = classificar_documento(nome_arquivo)
            
            # Monta um "dicionário" Python com os dados
            documento = {
                "nome_arquivo": nome_arquivo,
                "tipo_documento": tipo,
                "texto_completo": texto
            }
            
            # Adiciona o dicionário na nossa lista
            base_de_dados.append(documento)

    # --- Salvar o resultado ---
    # Fora do loop, depois que todos os PDFs foram processados
    print(f"\nSalvando dados extraídos em '{ARQUIVO_SAIDA}'...")
    
    with open(ARQUIVO_SAIDA, 'w', encoding='utf-8') as f:
        # Usa a biblioteca JSON para salvar a lista no arquivo
        # indent=4 deixa o arquivo formatado e legível
        json.dump(base_de_dados, f, indent=4, ensure_ascii=False)

    print(f"Sucesso! {len(base_de_dados)} documentos foram processados.")

    