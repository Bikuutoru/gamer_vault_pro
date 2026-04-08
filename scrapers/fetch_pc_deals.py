import requests
import json
import os
import time

def fetch_steam_deals():
    """
    Busca ofertas da Steam via CheapShark API, agora com chunking para processar
    lotes maiores sem acionar os Rate Limits da Steam.
    """
    # Endpoint da CheapShark para Steam (storeID=1) com pageSize aumentado para escalar
    url = "https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=50&pageSize=120"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        deals = response.json()
        
        formatted_deals = []
        regions = ['br', 'tr', 'ar']
        
        # Filtra apenas os deals que tem steamAppID
        valid_deals = [d for d in deals if d.get('steamAppID')]
        
        print(f"Buscando metadados regionais na Steam para {len(valid_deals)} ofertas...")
        
        # Chunking: Fatiar a lista em blocos de 30 para não estourar o limite da Steam
        chunk_size = 30
        for i in range(0, len(valid_deals), chunk_size):
            chunk = valid_deals[i:i+chunk_size]
            steam_app_ids = [str(d.get('steamAppID')) for d in chunk]
            app_ids_str = ",".join(steam_app_ids)
            
            regional_prices = {}
            try:
                for cc in regions:
                    steam_url = f"https://store.steampowered.com/api/appdetails?appids={app_ids_str}&cc={cc}&filters=price_overview"
                    res = requests.get(steam_url)
                    if res.status_code == 200:
                        regional_prices[cc] = res.json()
                    # Aguarda uns milissegundos para nao gerar throttling
                    time.sleep(0.2)
            except Exception as e:
                print(f"Aviso: Falha ao buscar dados de região no chunk {i}")

            for deal in chunk:
                app_id = str(deal.get('steamAppID'))
                
                brl_data = regional_prices.get('br', {}).get(app_id, {}).get('data', {}).get('price_overview', {})
                try_data = regional_prices.get('tr', {}).get(app_id, {}).get('data', {}).get('price_overview', {})
                ars_data = regional_prices.get('ar', {}).get(app_id, {}).get('data', {}).get('price_overview', {})

                real_brl = (brl_data.get('final') / 100) if brl_data.get('final') else round(float(deal.get('salePrice', 0)) * 5.0, 2)
                real_try = (try_data.get('final') / 100) if try_data.get('final') else round(float(deal.get('salePrice', 0)) * 32.0, 2)
                real_ars = (ars_data.get('final') / 100) if ars_data.get('final') else round(float(deal.get('salePrice', 0)) * 1000.0, 2)

                formatted_deals.append({
                    "title": deal.get('title'),
                    "store": "Steam",
                    "deal_id": deal.get('dealID'),
                    "game_id": deal.get('gameID'),
                    "steam_app_id": app_id,
                    "price": {
                        "sale_price_usd": float(deal.get('salePrice', 0)),
                        "normal_price_usd": float(deal.get('normalPrice', 0)),
                        "savings_percent": round(float(deal.get('savings', 0)), 2),
                        "regional": {
                            "BRL": real_brl,
                            "TRY": real_try,
                            "ARS": real_ars
                        }
                    },
                    "metacritic_score": deal.get('metacriticScore'),
                    "thumb": deal.get('thumb'),
                    "url": f"https://www.cheapshark.com/redirect?dealID={deal.get('dealID')}",
                    "store_url": f"https://store.steampowered.com/app/{app_id}"
                })
            
            # Pausa para preservar o endpoint rate publico
            time.sleep(1)
            
        return formatted_deals

    except Exception as e:
        print(f"Erro ao buscar ofertas da Steam: {e}")
        return []

if __name__ == "__main__":
    print("Iniciando coleta de ofertas da Steam (Modo Live Scale)...")
    deals = fetch_steam_deals()
    
    output_path = os.path.join(os.path.dirname(__file__), "../db/steam_deals_cache.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(deals, f, indent=4, ensure_ascii=False)
        
    print(f"Sucesso! {len(deals)} ofertas da Steam processadas e integradas.")
