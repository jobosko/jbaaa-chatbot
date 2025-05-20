from flask import Flask, render_template, request, jsonify
from database import buscar_debito
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lgpd')
def termos_lgpd():
    with open('lgpd_terms.txt', 'r', encoding='utf-8') as f:
        termos = f.read()
    return jsonify({'termos': termos})

@app.route('/verificar_cpf', methods=['POST'])
def verificar_cpf():
    cpf = request.json.get('cpf', '').replace('.', '').replace('-', '')
    
    if not re.match(r'^\d{11}$', cpf):
        return jsonify({'status': 'erro', 'mensagem': 'CPF inválido. Deve conter 11 dígitos numéricos.'})
    
    resultado = buscar_debito(cpf)
    
    if resultado is None:
        return jsonify({'status': 'nao_encontrado'})
    elif resultado['divida'] == 0:
        return jsonify({'status': 'sem_divida'})
    else:
        return jsonify({'status': 'com_divida', 'dados': resultado})

@app.route('/negociar', methods=['POST'])
def negociar():
    opcao = request.json.get('opcao')
    valor = float(request.json.get('valor'))

    if opcao == 'avista':
        return jsonify({'mensagem': f'Pagamento à vista disponível: R$ {valor:.2f} via PIX ou boleto.'})
    elif opcao == 'parcelar':
        parcelas = [3, 6, 12]
        simulacoes = {f"{p}x": f"R$ {(valor / p):.2f}" for p in parcelas}
        return jsonify({'mensagem': 'Simulações de parcelamento:', 'simulacoes': simulacoes})
    else:
        return jsonify({'mensagem': 'Opção inválida.'})

if __name__ == '__main__':
    app.run(debug=True)
