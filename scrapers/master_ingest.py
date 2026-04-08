import os
import subprocess
import time
import requests
import json

def fetch_exchange_rates():
    """
    Busca as taxas de conversão atuais de Dólar para outras moedas 
    para o recurso custom de 'convert_to' (API Premium).
    """
    db_path = os.path.join(os.path.dirname(__file__), "../db")
    if not os.path.exists(db_path):
        os.makedirs(db_path)
        
    try:
        res = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        if res.status_code == 200:
            rates = res.json().get('rates', {})
            output_path = os.path.join(os.path.dirname(__file__), "../db/exchange_rates.json")
            with open(output_path, "w") as f:
                json.dump(rates, f)
            print("Sucesso: Taxas de câmbio base (USD) atualizadas para a API.")
    except Exception as e:
        print("Aviso: Falha ao atualizar taxas de câmbio.")

def run_scraper(name, path):
    print(f"--- Rodando {name} ---")
    try:
        result = subprocess.run(["python", path], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Sucesso: {result.stdout.strip()}")
        else:
            print(f"Erro em {name}: {result.stderr.strip()}")
    except Exception as e:
        print(f"Falha ao executar {name}: {e}")

if __name__ == "__main__":
    start_time = time.time()
    print("=== GamerVault Master Ingestor v1.0 ===")
    
    base_dir = os.path.dirname(__file__)
    
    # Lista de scrapers para rodar
    scrapers = [
        ("Epic Freebies", os.path.join(base_dir, "monitor_freebies.py")),
        ("Steam Deals", os.path.join(base_dir, "fetch_pc_deals.py"))
    ]
    
    for name, path in scrapers:
        run_scraper(name, path)
        
    print("--- Atualizando Câmbio ---")
    fetch_exchange_rates()
        
    duration = time.time() - start_time
    print(f"\n=== Ingestão Completa em {duration:.2f}s ===")
