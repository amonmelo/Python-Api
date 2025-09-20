#!/usr/bin/env python3
import os
import secrets

ENV_FILE = ".env"
ENV_EXAMPLE_FILE = ".env.example"

def safe_input(prompt: str, default: str) -> str:
    try:
        val = input(prompt)
    except EOFError:
        # sem TTY (CI/CD) -> usar default
        return default
    val = (val or "").strip()
    return val if val else default

def setup_jwt():
    print("== Configuracao do JWT ==")
    print("1) Usar padrao seguro (DEV)")
    print("2) Digitar um segredo personalizado")
    print("3) Gerar um segredo aleatorio forte")
    choice = safe_input("Escolha 1/2/3 [1]: ", "1")

    if choice == "1":
        jwt_secret = "JWT_AUTENTICACAO_PROTEGIDA_LOCKED!"
        print("[setup] Usando segredo padrao de DEV.")
    elif choice == "2":
        jwt_secret = safe_input("Digite seu segredo JWT: ", "JWT_AUTENTICACAO_PROTEGIDA_LOCKED!")
        if not jwt_secret:
            print("[setup] Nenhum segredo informado, usando padrao.")
            jwt_secret = "JWT_AUTENTICACAO_PROTEGIDA_LOCKED!"
    elif choice == "3":
        jwt_secret = secrets.token_hex(32)
        print("[setup] Segredo aleatorio gerado.")
    else:
        print("[setup] Opcao invalida, usando padrao.")
        jwt_secret = "JWT_AUTENTICACAO_PROTEGIDA_LOCKED!"

    exp_default = "60"
    exp_input = safe_input(f"Minutos de expiracao do token [{exp_default}]: ", exp_default)
    jwt_exp = exp_input if exp_input.isdigit() else exp_default
    return jwt_secret, jwt_exp

def main():
    print("== Setup do Projeto ==")
    print("1) Instalacao padrao (default)")
    print("2) Instalacao customizada")
    mode = safe_input("Escolha 1/2 [1]: ", "1")

    if mode == "1":
        jwt_secret = "JWT_AUTENTICACAO_PROTEGIDA_LOCKED!"
        jwt_exp = "60"
        print("[setup] Instalacao padrao selecionada.")
    elif mode == "2":
        print("== Instalacao customizada ==")
        jwt_secret, jwt_exp = setup_jwt()
    else:
        print("[setup] Opcao invalida, caindo no padrao.")
        jwt_secret = "JWT_AUTENTICACAO_PROTEGIDA_LOCKED!"
        jwt_exp = "60"

    env_content = f"JWT_SECRET={jwt_secret}\nJWT_EXP_MINUTES={jwt_exp}\n"
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write(env_content)

    example_content = "JWT_SECRET=SEU_SEGREDO_AQUI\nJWT_EXP_MINUTES=60\n"
    with open(ENV_EXAMPLE_FILE, "w", encoding="utf-8") as f:
        f.write(example_content)

    print("\n[setup] Arquivo .env configurado com sucesso.")

if __name__ == "__main__":
    main()
