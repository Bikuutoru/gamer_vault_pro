# 🎮 GamerVault Pro (PC Deals Edition)

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Platform](https://img.shields.io/badge/platform-PC%20%7C%20Steam%20%7C%20Epic-blueviolet)

O **GamerVault Pro** é a arquitetura back-end hiper-otimizada que alimenta a [RapidAPI: GamerVault Pro](https://rapidapi.com/). A API foi meticulosamente refatorada para ser o **padrão ouro em rastreamento do ecossistema de PC Gaming**.

## 🔥 Por que Focamos em PC?
Abordagens multi-console exigem malabarismos complexos com web scraping bloqueado (proteções pesadas da PlayStation Store, etc). Decidimos adotar a filosofia de **"Bala de Prata"**. Nós processamos apenas a **Steam e a Epic Games**, mas o fazemos com uma precisão assustadora.

1. **Epic Freebies Checker:** Varredura algorítmica para detectar campanhas oficiais de "100% OFF" na Epic Games Store no segundo em que viram o relógio de quinta-feira. Ideal para Bots de Discord que marcam `@everyone`.
2. **Steam Native Regional Pricing:** Você não verá "dólar * taxa de conversão". Nosso worker entra em lote na `store.steampowered.com/api` e injeta os preços reais praticados da Argentina (ARS), Turquia (TRY) e Brasil (BRL).
3. **Live FX Convert_to:** Usando cache global de câmbio a cada 6h, permitimos aos usuários Premium traduzirem instantaneamente ofertas Lira Turca para Euro com zero latência (parâmetro `convert_to`).

---

## 🏗 Arquitetura do Sistema

A solução usa a força assíncrona do Node aliado a Workers em Python para scraping sujo.

### 1. The Workers (Scrapers em Python 🐍)
- `monitor_freebies.py`: Consome a federação GraphQL da Epic Games em tempo real.
- `fetch_pc_deals.py`: Consulta centenas de jogos com baixos preços na *CheapShark* e cruza o `AppID` nativo contra a API da Steam para preencher "clusters" hiper-valiosos em ARS e TRY.
- `master_ingest.py`: O orquestrador implacável. Roda de hora em hora via Cron (Render) populando nosso mini-banco de dados JSON em disco. Acopla um fetcher aberto de câmbio.

### 2. The Hub (API em Node.js 🟩)
Servidor minimalista usando Express que faz a varredura ultra-rápida (5 a 15ms de latência) nos arquivos cacheados JSON.

---

## 🛠 Como Rodar (Desenvolvimento Local)

### Passo 1: Instale as Dependências
Python (para os Workers Ingestores):
```bash
pip install -r requirements.txt
```

Node (Para o Servidor Principal):
```bash
npm install
```

### Passo 2: Popule o Banco de Dados (Gerando Cache)
Nossa tecnologia gira em torno de caches persistentes de altíssima velocidade. Antes de subir o Node.js, execute a ingestão mestra:
```bash
python scrapers/master_ingest.py
```
Isso vai criar e popular os arquivos `.json` essenciais na pasta `db/`.

### Passo 3: Inicie o Node.js Server
Temos monitoramento com Nodemon em fase de Dev. Verifique se copiou a env:
```bash
cp .env.example .env
npm run dev
```

Sua API purista de PC estará viva na porta definida!

---

## 🔒 Segurança em Produção
Este pacote foi arquitetado para ir para a RapidAPI. Logo, protegemos todo o roteador Express contra by-pass de porta direta usando o header oficial `X-RapidAPI-Proxy-Secret`.
Qualquer solicitação que não contenha esse hash em produção, ou as que vierem com query params do Tier pago (`currency`) num modelo aberto, são rejeitadas suavemente.

> *"Para quem rastreia ofertas de jogos e constrói as maiores comunidades do Discord, latência e precisão nas moedas argentinas/turcas são leis."* — GamerVault Architecture Design.
