import requests
import json
import os

def fetch_epic_freebies():
    """
    Scraper para a Epic Games Store Freebies usando a API pública (não oficial).
    """
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        games = data['data']['Catalog']['searchStore']['elements']
        freebies = []
        
        for game in games:
            # Filtro para verificar se o jogo está atualmente gratuito ou será em breve
            promotions = game.get('promotions')
            if not promotions:
                continue
            
            offer_type = game.get('offerType')
            title = game.get('title')
            
            # Checar se o preço atual é 0
            price_info = game.get('price', {}).get('totalPrice', {})
            discount_price = price_info.get('discountPrice', -1)
            
            if discount_price == 0:
                freebies.append({
                    "title": title,
                    "id": game.get('id'),
                    "description": game.get('description'),
                    "store": "Epic Games Store",
                    "url": f"https://www.epicgames.com/store/en-US/p/{game.get('productSlug') or game.get('urlSlug')}",
                    "image": game.get('keyImages', [{}])[0].get('url'),
                    "status": "Currently Free"
                })
        
        return freebies

    except Exception as e:
        print(f"Erro ao buscar freebies da Epic: {e}")
        return []

if __name__ == "__main__":
    print("Iniciando monitoramento de jogos grátis...")
    free_games = fetch_epic_freebies()
    
    # Simulação de salvamento no DB local (JSON para teste)
    output_path = os.path.join(os.path.dirname(__file__), "../db/freebies_cache.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(free_games, f, indent=4, ensure_ascii=False)
        
    print(f"Sucesso! {len(free_games)} jogos grátis encontrados na Epic Games Store.")
