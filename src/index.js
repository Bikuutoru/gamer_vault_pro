require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Swagger Documentation
const swaggerDocument = YAML.load(path.join(__dirname, '../openapi.yaml'));
app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// Global Header Middleware (RapidAPI Proxy Secret Protection)
app.use((req, res, next) => {
    const proxySecret = req.get('X-RapidAPI-Proxy-Secret');
    // Em produção, habilitar esta checagem para segurança
    if (!proxySecret && process.env.NODE_ENV === 'production') {
        return res.status(403).json({ error: 'Forbbiden: Invalid Proxy Secret' });
    }
    next();
});

// Routes
const apiRoutes = require('./routes');
app.use('/api/v1', apiRoutes);

// Root redirect to docs
app.get('/', (req, res) => {
    res.redirect('/docs');
});

app.listen(PORT, () => {
    console.log(`[GamerVault Pro] Server running at http://localhost:${PORT}`);
    console.log(`[GamerVault Pro] Documentation: http://localhost:${PORT}/docs`);
});
