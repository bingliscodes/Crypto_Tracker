#!/bin/bash
cd /Users/benjamininglis/Code/mentorship/projects/Crypto_Tracker
source .venv/bin/activate
cd src
STORAGE_MODE="mongodb" DATA_SOURCE="coinmarketcap" app/scripts/get_crypto_prices.py