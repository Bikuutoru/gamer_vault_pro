import json
import os

def fetch_psn_deals():
    """
    Simula a coleta de ofertas da PSN.
    """
    mock_deals = [
        {
            "title": "Marvel's Spider-Man 2",
            "store": "PSN",
            "price": {
                "sale_price_usd": 49.69,
                "normal_price_usd": 69.99,
                "savings_percent": 29,
                "regional": {
                    "BRL": 249.50,
                    "TRY": 899.00,
                    "ARS": 24999.00
                }
            },
            "url": "https://www.playstation.com/en-us/games/marvels-spider-man-2/",
            "thumb": "https://image.api.playstation.com/vulcan/ap/rnd/202306/1219/6013234d65bc836742336f33d455d65f.png"
        },
        {
            "title": "Elden Ring",
            "store": "PSN",
            "price": {
                "sale_price_usd": 35.99,
                "normal_price_usd": 59.99,
                "savings_percent": 40,
                "regional": {
                    "BRL": 179.90,
                    "TRY": 599.00,
                    "ARS": 15999.00
                }
            },
            "url": "https://www.playstation.com/en-us/games/elden-ring/",
            "thumb": "https://image.api.playstation.com/vulcan/ap/rnd/202110/2000/aajm89u3c3a9j3u003.png"
        }
    ]
    return mock_deals

def fetch_xbox_deals():
    """
    Simula a coleta de ofertas da Xbox Store e Game Pass.
    """
    mock_deals = [
        {
            "title": "Forza Horizon 5",
            "store": "Xbox",
            "price": {
                "sale_price_usd": 29.99,
                "normal_price_usd": 59.99,
                "savings_percent": 50,
                "regional": {
                    "BRL": 124.50,
                    "TRY": 449.00,
                    "ARS": 11000.00
                }
            },
            "url": "https://www.xbox.com/en-us/games/forza-horizon-5",
            "thumb": "https://store-images.s-microsoft.com/image/apps.50650.14441005315132515.22233b82-62a2-4754-b52f-149c951e604f.b0051e50-0255-44f3-b962-d27803e62058"
        },
        {
            "title": "Halo Infinite",
            "store": "Xbox",
            "price": {
                "sale_price_usd": 19.99,
                "normal_price_usd": 59.99,
                "savings_percent": 66,
                "regional": {
                    "BRL": 99.00,
                    "TRY": 299.00,
                    "ARS": 6500.00
                }
            },

            "url": "https://www.xbox.com/en-us/games/halo-infinite",
            "thumb": "https://store-images.s-microsoft.com/image/apps.10.13510798887910545.999f8dbe-89ee-475a-a70d-8389366c8f61.12345678-1234-1234-1234-123456789012"
        }
    ]
    return mock_deals

if __name__ == "__main__":
    print("Iniciando coleta de ofertas de Consoles (Mock Fallback)...")
    deals = fetch_psn_deals() + fetch_xbox_deals()
    
    output_path = os.path.join(os.path.dirname(__file__), "../db/console_deals_cache.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(deals, f, indent=4, ensure_ascii=False)
        
    print(f"Sucesso! {len(deals)} ofertas de console processadas.")
