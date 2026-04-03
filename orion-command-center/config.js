require('dotenv').config();

module.exports = {
  OLLAMA_URL: process.env.OLLAMA_URL || 'http://localhost:11434/v1',
  MODEL_NAME: process.env.MODEL_NAME || 'gemma2:27b',
  USER_PROFILE: {
    osPreference: 'Detect at Runtime',
    defaultTools: ['openApp', 'getSystemStatus', 'listDirectory']
  }
};
