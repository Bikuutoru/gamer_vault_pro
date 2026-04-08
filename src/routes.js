const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');

// Helper para ler cache
const readCache = (filename) => {
    const filePath = path.join(__dirname, '../db', filename);
    if (!fs.existsSync(filePath)) return [];
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
};

/**
 * @route GET /api/v1/deals/freebies
 */
router.get('/deals/freebies', (req, res) => {
    try {
        const freebies = readCache('freebies_cache.json');
        res.json(freebies);
    } catch (error) {
        res.status(500).json({ error: 'Erro ao processar jogos gratuitos' });
    }
});

/**
 * @route GET /api/v1/deals/latest
 */
router.get('/deals/latest', (req, res) => {
    try {
        const steamDeals = readCache('steam_deals_cache.json');
        
        const allDeals = [...steamDeals];
        
        // Logica de Filtro por Loja
        const storeFilter = req.query.store;
        let filtered = allDeals;
        if (storeFilter) {
            filtered = allDeals.filter(d => d.store.toLowerCase() === storeFilter.toLowerCase());
        }

        // --- LÓGICA PREMIUM (MULTIMOEDA) ---
        // Filtragem de dados regionais para não entregar de graça o que é benefício PRO
        const premiumCurrencies = ['BRL', 'TRY', 'ARS'];
        const currency = req.query.currency ? req.query.currency.toUpperCase() : 'USD';
        const convertTo = req.query.convert_to ? req.query.convert_to.toUpperCase() : null;
        const rates = readCache('exchange_rates.json');
        
        const processedDeals = filtered.map(deal => {
            const d = { ...deal };
            
            // Se o request é USD ou uma moeda não mapeada, devolvemos sem o cluster regional
            if (!premiumCurrencies.includes(currency)) {
                if (d.price && d.price.regional) delete d.price.regional;
            } else {
                // Manutenção MVP: Trazemos os valores na moeda alvo. 
                // Se foi fornecido o convert_to, operamos a conversão live do dado regional para a moeda fiat solicitada
                if (convertTo && rates[currency] && rates[convertTo]) {
                    if (d.price && d.price.regional && d.price.regional[currency]) {
                        // Converte o valor regional (ex: 25000 ARS) para USD base, e depois multiplica para a moeda desejada
                        const rawRegionalValue = d.price.regional[currency];
                        const usdCalculated = rawRegionalValue / rates[currency];
                        const convertedFiatValue = usdCalculated * rates[convertTo];
                        
                        // Acrescenta novo nó customizado
                        d.price.regional[`converted_to_${convertTo}`] = parseFloat(convertedFiatValue.toFixed(2));
                    }
                }
            }
            return d;
        });

        res.json(processedDeals);
    } catch (error) {
        res.status(500).json({ error: 'Erro ao processar ofertas' });
    }
});

/**
 * @route GET /api/v1/deals/search
 */
router.get('/deals/search', async (req, res) => {
    const query = req.query.q;
    if (!query) return res.status(400).json({ error: 'Query parameter "q" is required' });

    try {
        // LIVE SEARCH: Bate em tempo real direto na CheapShark 
        // em vez de consultar a limitadíssima base cacheada
        const cheapSharkUrl = `https://www.cheapshark.com/api/1.0/deals?title=${encodeURIComponent(query)}&sortBy=Price`;
        const response = await fetch(cheapSharkUrl);
        const deals = await response.json();

        // Filtrar e mapear apenas Lojas alvo (1=Steam, 7=GOG, 11=Epic)
        const validStoreIds = ['1', '7', '11'];
        const filtered = deals.filter(d => validStoreIds.includes(d.storeID));

        const storeMap = { '1': 'Steam', '7': 'GOG', '11': 'Epic Games Store' };

        const results = filtered.map(deal => ({
            title: deal.title,
            store: storeMap[deal.storeID] || "PC Store",
            deal_id: deal.dealID,
            game_id: deal.gameID,
            steam_app_id: deal.steamAppID || null,
            price: {
                sale_price_usd: parseFloat(deal.salePrice || 0),
                normal_price_usd: parseFloat(deal.normalPrice || 0),
                savings_percent: parseFloat(deal.savings ? parseFloat(deal.savings).toFixed(2) : 0)
            },
            metacritic_score: deal.metacriticScore,
            thumb: deal.thumb,
            url: `https://www.cheapshark.com/redirect?dealID=${deal.dealID}`,
            store_url: deal.steamAppID && deal.storeID === '1' ? `https://store.steampowered.com/app/${deal.steamAppID}` : null
        }));

        res.json(results);
    } catch (error) {
        console.error("Live Search Error:", error);
        res.status(500).json({ error: 'Erro na busca em tempo real' });
    }
});

module.exports = router;
