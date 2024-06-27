import requests
import re
import string
import argparse
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Função para validar se a chave já está em uso na Steam (simulação)
def is_key_in_use(api_key, key_candidate):
    response = requests.get(f"https://api.steampowered.com/ISteamUser/IsSteamKeyInUse/v1/?key={api_key}&steam_key={key_candidate}")
    if response.status_code == 200:
        data = response.json()
        if "error" in data:
            return False  # Chave não está em uso
        else:
            return True   # Chave está em uso
    else:
        return False  # Falha na requisição

# Simulação de uma lista de jogos instalados pelo usuário
def get_installed_games(steam_id):
    installed_games = [
        "DayZ",
        "Counter-Strike: Global Offensive",
        "The Witcher 3: Wild Hunt",
        "Grand Theft Auto V",
        "PlayerUnknown's Battlegrounds"
    ]
    return installed_games

def extract_patterns(example_keys):
    length = len(example_keys[0])
    char_set = string.ascii_uppercase + string.digits
    pattern = re.compile(f"^[{re.escape(char_set)}]{{{length}}}$")
    return {"length": length, "char_set": char_set, "pattern": pattern}

def generate_key_candidate(patterns, user_data, installed_games):
    length = patterns["length"]
    char_set = patterns["char_set"]
    key_candidate = ''.join(random.choices(char_set, k=length))

    game_related_to_key = "DayZ"  # Substitua pela lógica real para determinar o jogo relacionado à chave
    while game_related_to_key in installed_games:
        key_candidate = ''.join(random.choices(char_set, k=length))
        game_related_to_key = "DayZ"  # Atualize o jogo relacionado à chave com base na nova chave gerada

    return key_candidate

def refine_key_candidate(key_candidate, validation_response):
    invalid_chars = validation_response.get("invalid_chars", [])
    char_set = ''.join(set(string.ascii_uppercase + string.digits) - set(invalid_chars))
    key_candidate = ''.join(random.choices(char_set, k=len(key_candidate)))
    return key_candidate

def validate_steam_key(key_candidate):
    return re.match(r"^[A-Z0-9]{15}$", key_candidate) is not None

def simulate_sensitive_monitoring(user_data):
    steam_id = user_data["steam_id"]
    installed_games = get_installed_games(steam_id)
    print(f"Jogos instalados para o usuário {user_data['user_name']}: {', '.join(installed_games)}")

def generate_steam_key(user_data):
    example_keys = [
        "ABCDE-FGHIJ-KLMNO",
        "PQRST-UVWXY-Z1234",
        "56789-ABCDE-FGHIJ",
        "KLMNO-PQRST-UVWXY",
        "Z1234-56789-ABCDE",
        "FGHIJ-KLMNO-PQRST",
        "UVWXY-Z1234-56789",
        "ABCDE-FGHIJ-KLMNO",
        "PQRST-UVWXY-Z1234",
        "56789-ABCDE-FGHIJ",
        "KLMNO-PQRST-UVWXY",
        "Z1234-56789-ABCDE",
        "FGHIJ-KLMNO-PQRST",
        "UVWXY-Z1234-56789",
        "ABCDE-FGHIJ-KLMNO",
        "PQRST-UVWXY-Z1234",
        "56789-ABCDE-FGHIJ",
        "KLMNO-PQRST-UVWXY",
        "Z1234-56789-ABCDE",
        "FGHIJ-KLMNO-PQRST"
    ]

    patterns = extract_patterns(example_keys)

    simulate_sensitive_monitoring(user_data)

    installed_games = get_installed_games(user_data["steam_id"])

    key_candidate = generate_key_candidate(patterns, user_data, installed_games)
    steam_api_key = user_data['api_key']

    is_valid = validate_steam_key(key_candidate)
    while not is_valid or is_key_in_use(steam_api_key, key_candidate) or any(game in key_candidate for game in installed_games):
        validation_response = {"invalid_chars": ["Q", "Z", "1"]}
        key_candidate = refine_key_candidate(key_candidate, validation_response)
        is_valid = validate_steam_key(key_candidate)

    return key_candidate

def parse_arguments():
    parser = argparse.ArgumentParser(description="Acesso à Conta Steam")
    parser.add_argument("--user-name", type=str, required=True, help="Nome de usuário da Steam")
    parser.add_argument("--password", type=str, required=True, help="Senha da conta Steam")
    parser.add_argument("--api-key", type=str, required=True, help="Chave de API da Steam do usuário")
    parser.add_argument("--steam-login-secure", type=str, required=True, help="Valor do cookie steamLoginSecure")
    parser.add_argument("--session-id", type=str, required=True, help="ID da sessão da Steam")
    args = parser.parse_args()
    return {
        "user_name": args.user_name,
        "password": args.password,
        "api_key": args.api_key,
        "steam_login_secure": args.steam_login_secure,
        "session_id": args.session_id,
        "steam_id": args.user_name  # Assume that steam_id is same as user_name for simulation purposes
    }

# Função para conectar à conta Steam
def connect_to_steam(user_data):
    print("Tentando conectar à conta Steam...")
    connected = True  # Simulação de sucesso na conexão
    if connected:
        print("Conectado com sucesso.")
        return True
    else:
        print("Falha na conexão. Tente novamente.")
        return False

# Função para escanear a biblioteca de jogos do usuário
def scan_library(user_data):
    print("Escaneando a biblioteca de jogos...")
    library = {
        "total_games": 50,
        "free_games": 10,
        "purchased_games": 40
    }
    print(f"Total de jogos: {library['total_games']}")
    print(f"Jogos gratuitos: {library['free_games']}")
    print(f"Jogos comprados: {library['purchased_games']}")
    return library

# Função para treinar um modelo de regressão logística para validar chaves Steam
def train_validation_model():
    # Simulação de dados de treinamento
    data = {
        'key': [
            'ABCDE-FGHIJ-KLMNO', 'PQRST-UVWXY-Z1234', '56789-ABCDE-FGHIJ', 
            'KLMNO-PQRST-UVWXY', 'Z1234-56789-ABCDE', 'FGHIJ-KLMNO-PQRST',
            'UVWXY-Z1234-56789', 'ABCDE-FGHIJ-KLMNO', 'PQRST-UVWXY-Z1234',
            '56789-ABCDE-FGHIJ', 'KLMNO-PQRST-UVWXY', 'Z1234-56789-ABCDE',
            'FGHIJ-KLMNO-PQRST', 'UVWXY-Z1234-56789', 'ABCDE-FGHIJ-KLMNO',
            'PQRST-UVWXY-Z1234', '56789-ABCDE-FGHIJ', 'KLMNO-PQRST-UVWXY',
            'Z1234-56789-ABCDE', 'FGHIJ-KLMNO-PQRST'
        ],
        'valid': [
            1, 1, 0, 1, 0, 1, 0, 1, 1, 0,
            1, 0, 1, 0, 1, 1, 0, 1, 0, 1
        ]
    }

    df = pd.DataFrame(data)
    X = df['key'].apply(lambda x: [ord(char) for char in x.replace('-', '')]).tolist()
    y = df['valid']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    print(f"Acurácia do modelo de validação: {model.score(X_test, y_test) * 100:.2f}%")

    return model

# Função principal
def main():
    user_data = parse_arguments()
    
    connected = connect_to_steam(user_data)
    if not connected:
        return
    
    validation_model = train_validation_model()

    while True:
        print("\nMenu:")
        print("1. Scanear biblioteca atual")
        print("2. Gerar chaves Steam")
        print("3. Sair")
        choice = input("Escolha uma opção: ")
        
        if choice == "1":
            scan_library(user_data)
        elif choice == "2":
            generated_key = generate_steam_key(user_data)
            print("Chave Steam gerada:", generated_key)
        elif choice == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
