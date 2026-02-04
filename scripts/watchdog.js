const { spawn } = require('child_process');
const path = require('path');

// --- CONFIGURATION ---
// Chemin vers l'entry point de clawdbot
const ENTRY_JS = 'C:\\Users\\COVAGE\\AppData\\Roaming\\npm\\node_modules\\clawdbot\\dist\\entry.js';
const ARGS = ['gateway', '--port', '18789'];

// --- LOGIQUE DE SURVEILLANCE ---
function startBot() {
    console.log(`[${new Date().toISOString()}] 🍷 Le Cardinal : Lancement de la passerelle...`);

    const bot = spawn('node', [ENTRY_JS, ...ARGS], {
        stdio: 'inherit',
        shell: true,
        env: {
            ...process.env,
            TELEGRAM_BOT_TOKEN: '8329329963:AAG0dgY6Gi2iGZjTKj_jwQrtw7S70ghDMxM' // Token centralisé
        }
    });

    bot.on('exit', (code) => {
        console.log(`[${new Date().toISOString()}] ⚠️ Cardinal arrêté (Code: ${code}). Relance automatique dans 5s...`);
        setTimeout(startBot, 5000);
    });

    bot.on('error', (err) => {
        console.error('❌ Erreur Critique Sentinelle:', err);
        setTimeout(startBot, 10000);
    });
}

console.log('--- 🛡️ SENTINELLE DU CARDINAL ACTIVÉE ---');
startBot();
