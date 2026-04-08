import requests
import json
import os

def fetch_epic_freebies():
    """
    Scraper para a Epic Games Store Freebies usando a API pública (não oficial).
    Agora com lógica de Slug aprimorada para evitar erro 404.
    """
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        games = data['data']['Catalog']['searchStore']['elements']
        freebies = []
        
        for game in games:
            title = game.get('title')
            promotions = game.get('promotions')
            if not promotions:
                continue
            
            # Checar se o preço atual é 0 (Free)
            price_info = game.get('price', {}).get('totalPrice', {})
            discount_price = price_info.get('discountPrice', -1)
            
            # --- Lógica de Slug Robusta ---
            # 1. Tenta productSlug direto
            slug = game.get('productSlug')
            
            # 2. Se falhar, busca no nested offerMappings (padrão atual da Epic para freebies)
            if not slug or "-" not in slug:
                mappings = game.get('offerMappings', [])
                if mappings:
                    slug = mappings[0].get('pageSlug')
            
            # 3. Fallback final para urlSlug
            if not slug:
                slug = game.get('urlSlug')

            if discount_price == 0:
                # URL no padrão store.epicgames.com/en-US/p/slug
                final_url = f"https://store.epicgames.com/en-US/p/{slug}"
                
                freebies.append({
                    "title": title,
                    "id": game.get('id'),
                    "description": game.get('description'),
                    "store": "Epic Games Store",
                    "url": final_url,
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
    
    output_path = os.path.join(os.path.dirname(__file__), "../db/freebies_cache.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(free_games, f, indent=4, ensure_ascii=False)
        
    print(f"Sucesso! {len(free_games)} jogos grátis encontrados na Epic Games Store.")
    for g in free_games:
        print(f"- {g['title']}: {g['url']}")
