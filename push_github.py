import os
import subprocess

# === CONFIGURAÇÕES ===
REPO_URL = "https://github.com/jobosko/jbaaa-chatbot.git"
TOKEN_GITHUB = "ghp_SEU_TOKEN_AQUI"  # Substitua por seu token real
DIRETORIO_PROJETO = "jbaaa_chatbot_completo"

# Substitui https:// por https://<token>@ para autenticação via token
url_com_token = REPO_URL.replace("https://github.com/jobosko/jbaaa-chatbot.git", f"https://{TOKEN_GITHUB}@")

# Comandos Git
comandos = [
    f"cd {DIRETORIO_PROJETO}",
    "git init",
    f"git remote add origin {url_com_token}",
    "git add .",
    'git commit -m "Deploy inicial do chatbot JBAAA"',
    "git branch -M main",
    "git push -u origin main"
]

# Executa comandos
comando_final = " && ".join(comandos)
resultado = subprocess.run(comando_final, shell=True)

if resultado.returncode == 0:
    print("✅ Push realizado com sucesso!")
else:
    print("❌ Algo deu errado durante o push.")