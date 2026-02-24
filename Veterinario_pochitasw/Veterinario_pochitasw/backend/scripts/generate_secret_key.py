#!/usr/bin/env python
"""Script para generar una SECRET_KEY segura para Django"""
import secrets

if __name__ == "__main__":
    secret_key = secrets.token_urlsafe(50)
    print(f"\nTu SECRET_KEY generada:")
    print(f"{secret_key}\n")
    print("Cópiala y úsala en la variable de entorno DJANGO_SECRET_KEY")

