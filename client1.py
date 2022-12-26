'''
Simulacao de protocolo TCP utilizando UDP

A mensagem eh dividida em cabecalho e dados, no cabecalho e da forma xxxxxxxxyyyyyyyy, sendo x o SEQ e y o ACK,
o SEQ eh a posicao do primeiro byte enviado na mensagem completa (ex. SEQ(0,1,2,3,4) = Hello), e o ACK eh o 
numero do ultimo byte recebido (ex. se cliente enviar 'Hello', servidor retorna 4).
A funcao usada para receber mensagens tanto no cliente quanto no servidor eh o recvfrom, que retorna uma 
tupla (mensagem, informacao do remetente). A funcao decodificada retorna a string ['b{tupla}'], estando os ''
dentro da string.
No cliente eh usado um timeout para que o segmento seja reenviado se nao receber resposta depois do tempo
determinado. O servidor nao possui timeout, enviando respostas apenas depois de receber uma mensagem.
'''

import socket, time, math

msgFromClient       = "Hello UDP Server, Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Pharetra vel turpis nunc eget lorem dolor sed viverra ipsum. Leo a diam sollicitudin tempor id eu nisl nunc mi. Egestas congue quisque egestas diam. Nisi scelerisque eu ultrices vitae auctor eu augue ut lectus. Risus nec feugiat in fermentum posuere urna nec. Sed cras ornare arcu dui vivamus arcu felis bibendum. In fermentum posuere urna nec tincidunt. Ut eu sem integer vitae justo eget magna fermentum. Vitae nunc sed velit dignissim. Nam aliquam sem et tortor consequat. Lectus proin nibh nisl condimentum id venenatis a condimentum vitae. In cursus turpis massa tincidunt dui ut ornare lectus sit. Arcu bibendum at varius vel pharetra vel."
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 32                        # Tamanho total da mensagem enviada e recebida (header+msg)
headerSize          = 16                        # Tamanho do cabecalho
messageSize         = bufferSize - headerSize   # Tamanho dos dados
seq                 = 0                         # Numero do primeiro bite enviado na msg
ack                 = 0                         # ACK para resposta do servidor, indicando n do ultimo bite recebido

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # Cria Socket
UDPClientSocket.settimeout(1)               # Define timeout de 1000ms (reenvia msg se n recebe ack dps de Xms)


# Envia mensagem para servidor.
def sendMsg():
    seqStr = str(seq).rjust((round(headerSize/2)), '0') # Encaixa o SEQ no header (seq=11 header= 00000011yyyyyyyyy)
    ackStr = str(ack).rjust((round(headerSize/2)), '0') # Encaixa o ACK no header (ack=24 header= xxxxxxxx000000024)
    messageToSend = str.encode(seqStr + ackStr + msgFromClient[seq:seq+messageSize])    # Junta header e msg
    print(f'Enviado: {messageToSend}')                  
    UDPClientSocket.sendto(messageToSend, serverAddressPort)    # Envia para servidor
    print('--------------------------') 


# Loop principal
while (seq < len(msgFromClient)):       # Envia novos segmentos ate que a mensagem seja enviada completamente
    sendMsg()   
    try:                            # Tenta receber o ACK depois de enviar
        bytesAddressPair = UDPClientSocket.recvfrom(bufferSize)
    except socket.timeout:          # No caso do timeout acabar, ele inicia um novo ciclo do loop principal
        pass
    else:                           # Se uma msg for recebida, ela e armazenada em bytesAddressPair;
                                    # ela e uma tupla com (mensagem, informacoes do remetente);
                                    # sendo a mensagem e dividida em header e dados.
        if (bytesAddressPair):
            print(f'Recebido: {bytesAddressPair[0]}')
            recSeq = int(str(format(                                            # (00000011yyyyyyyy -> seq=11)
                    bytesAddressPair[0]))[2:2+round(headerSize/2)])             
            recAck = int(str(format(                                            # (xxxxxxxx00000024 -> ack=24)
                    bytesAddressPair[0]))[2+round(headerSize/2):2+headerSize])  
            if (recAck > ack):          # So atualiza ack se o ack recebido for maior que o armazenado;
                seq = recAck            # evitando que acks duplicados facam o cliente reenviar uma msg;
                ack = recSeq            # ja enviada.
            bytesAddressPair = None