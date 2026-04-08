const request = require('supertest');
const express = require('express');
const apiRoutes = require('../src/routes');

const app = express();
app.use(express.json());
app.use('/api/v1', apiRoutes);

describe('GamerVault Pro API Endpoints', () => {
    
    it('GET /api/v1/deals/freebies deve retornar jogos 100% grátis', async () => {
        const response = await request(app).get('/api/v1/deals/freebies');
        expect(response.status).toBe(200);
        expect(Array.isArray(response.body)).toBeTruthy();
        
        if (response.body.length > 0) {
            // Verifica a estrutura dos dados
            const firstGame = response.body[0];
            expect(firstGame).toHaveProperty('title');
            expect(firstGame).toHaveProperty('status', 'Currently Free');
        }
    });

    it('GET /api/v1/deals/latest deve funcionar com parâmetros multimoeda (Tier Pro)', async () => {
        // Simulando usuário que passa 'currency=BRL'
        const response = await request(app).get('/api/v1/deals/latest?currency=BRL');
        expect(response.status).toBe(200);
        expect(Array.isArray(response.body)).toBeTruthy();
    });

    it('GET /api/v1/deals/latest com USD (Moeda default/Free) esconde os dados regionais', async () => {
        const response = await request(app).get('/api/v1/deals/latest');
        expect(response.status).toBe(200);
        
        if (response.body.length > 0) {
            const firstDeal = response.body[0];
            // Se for do tipo Console (que mockamos com BRL) ou Steam, e o parâmetro não foi passado, regional = undefined
            if (firstDeal.price) {
                expect(firstDeal.price.regional).toBeUndefined();
            }
        }
    });

    it('GET /api/v1/deals/search falha graciosamente se nenhum "q" for passado', async () => {
        const response = await request(app).get('/api/v1/deals/search');
        expect(response.status).toBe(400);
        expect(response.body).toHaveProperty('error');
    });
});
