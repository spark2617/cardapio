from twilio.rest import Client

# Configuração do Twilio
def enviar_whatsapp_vendedor(pedido):
    # Substitua pelo seu SID da conta e token de autenticação
    account_sid = 'SEU_ACCOUNT_SID'
    auth_token = 'SEU_AUTH_TOKEN'
    client = Client(account_sid, auth_token)

    # Envia a mensagem via WhatsApp
    message = client.messages.create(
        body=f'Novo pedido recebido:\n\nCliente: {pedido.nome_do_cliente}\nEndereço: {pedido.endereco}\nContato: {pedido.contato_cliente}',
        from_='whatsapp:+14155238886',  # Número de WhatsApp do Twilio (sandbox ou registrado)
        to='whatsapp:+55XXXXXXXXXXX'  # Número do vendedor com código do país (exemplo: +55 para Brasil)
    )

    return message.sid  # Retorna o SID da mensagem enviada, pode ser usado para verificar o status

