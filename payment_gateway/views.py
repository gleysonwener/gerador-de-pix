import base64
import json
import uuid
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Order
from .forms import PaymentForm
import requests

import qrcode
from io import BytesIO
from decimal import Decimal

import crcmod
import qrcode
import os

API_URL = 'http://api.example.com/validate_credit_card'

def payment_form(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Se o usuário inseriu uma chave Pix, gere um código QR
            # if form.cleaned_data['pix_key']:
                # Crie as informações do pagamento Pix
            amount = str(form.cleaned_data['amount'])
            description = form.cleaned_data['description']
            pix_key = form.cleaned_data['pix_key']

            pix_data = {
                'chave': pix_key,
                'txid': str(uuid.uuid4()),  # ID da transação (geralmente único)
                'valor': amount,
                'descricao': description
            }
            

            # Crie a string com as informações do Pix
            pix_data2 = f"chave={pix_key}&txid=12345&valor={amount}&descricao={description}"

            print(pix_data)
            print(pix_data2)
            
            # Gere o código QR a partir dos dados do Pix
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(json.dumps(pix_data))
            qr.make(fit=True)
            
            # img = qr.make_image(fill_color="black", back_color="white")
            # buffered = BytesIO()
            # img.save(buffered, format="PNG")
            # pix_qr_code = base64.b64encode(buffered.getvalue()).decode("utf-8")

            qr_image = qr.make_image(fill_color="black", back_color="white")
            buffered = BytesIO()
            qr_image.save(buffered)
            qr_image_data = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            # Renderize o template com o código QR
            return render(request, 'payment_pix.html', {'pix_qr_code': qr_image_data})
            # return render(request, 'payment_pix.html', {'pix_qr_code': pix_qr_code})
        else:
            # Lógica para processamento de pagamento com cartão de crédito (como no exemplo anterior)
            if request.method == 'POST':
                form = PaymentForm(request.POST)
                if form.is_valid():
                    # Valide os dados do cartão de crédito com a API fictícia
                    card_data = {
                        'card_number': form.cleaned_data['card_number'],
                        'expiration_date': form.cleaned_data['expiration_date'],
                        'cvv': form.cleaned_data['cvv']
                    }
                    response = requests.post(API_URL, json=card_data)

                    if response.status_code == 200:
                        # Se a API de validação retornar sucesso, processe o pagamento
                        order = form.save()
                        return redirect('payment_confirmation', order_id=order.id)
                    else:
                        form.add_error(None, 'Erro na validação do cartão de crédito')
    else:
        form = PaymentForm()
    return render(request, 'payment_form.html', {'form': form})






def payment_confirmation(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'payment_gateway/payment_confirmation.html', {'order': order})





class Payload():
    def __init__(self, nome, chavepix, valor, cidade, txtId, diretorio=''):
        
        self.nome = nome
        self.chavepix = chavepix
        self.valor = valor.replace(',', '.')
        self.cidade = cidade
        self.txtId = txtId
        self.diretorioQrCode = diretorio

        self.nome_tam = len(self.nome)
        self.chavepix_tam = len(self.chavepix)
        self.valor_tam = len(self.valor)
        self.cidade_tam = len(self.cidade)
        self.txtId_tam = len(self.txtId)

        self.merchantAccount_tam = f'0014BR.GOV.BCB.PIX01{self.chavepix_tam:02}{self.chavepix}'
        self.transactionAmount_tam = f'{self.valor_tam:02}{float(self.valor):.2f}'

        self.addDataField_tam = f'05{self.txtId_tam:02}{self.txtId}'

        self.nome_tam = f'{self.nome_tam:02}'

        self.cidade_tam = f'{self.cidade_tam:02}'

        self.payloadFormat = '000201'
        self.merchantAccount = f'26{len(self.merchantAccount_tam):02}{self.merchantAccount_tam}'
        self.merchantCategCode = '52040000'
        self.transactionCurrency = '5303986'
        self.transactionAmount = f'54{self.transactionAmount_tam}'
        self.countryCode = '5802BR'
        self.merchantName = f'59{self.nome_tam:02}{self.nome}'
        self.merchantCity = f'60{self.cidade_tam:02}{self.cidade}'
        self.addDataField = f'62{len(self.addDataField_tam):02}{self.addDataField_tam}'
        self.crc16 = '6304'

  
    def gerarPayload(self):
        self.payload = f'{self.payloadFormat}{self.merchantAccount}{self.merchantCategCode}{self.transactionCurrency}{self.transactionAmount}{self.countryCode}{self.merchantName}{self.merchantCity}{self.addDataField}{self.crc16}'

        self.gerarCrc16(self.payload)

    
    def gerarCrc16(self, payload):
        crc16 = crcmod.mkCrcFun(poly=0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)

        self.crc16Code = hex(crc16(str(payload).encode('utf-8')))

        self.crc16Code_formatado = str(self.crc16Code).replace('0x', '').upper().zfill(4)

        self.payload_completa = f'{payload}{self.crc16Code_formatado}'

        self.gerarQrCode(self.payload_completa, self.diretorioQrCode)

    
    def gerarQrCode(self, payload, diretorio):
        dir = os.path.expanduser(diretorio)
        self.qrcode = qrcode.make(payload)
        self.qrcode.save(os.path.join(dir, 'pixqrcodegen.png'))
        
        return print(payload)


if __name__ == '__main__':
    # 12345678900 seria o formato do CPF sem pontos e traços
    Payload('Nome Sobrenome', '12345678900', '1.00', 'Cidade Ficticia', 'LOJA01').gerarPayload()
