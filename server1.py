import socket, time

localIP             = "127.0.0.1"
localPort           = 20001
bufferSize          = 32                        # Tamanho total da mensagem enviada e recebida (header+msg)
headerSize          = 16                        # Tamanho do cabecalho
messageSize         = bufferSize - headerSize   # Tamanho dos dados
msgFromServer       = 'HELLO UDP SERVER, LOREM IPSUM DOLOR SIT AMET, CONSECTETUR ADIPISCING ELIT, SED DO EIUSMOD TEMPOR INCIDIDUNT UT LABORE ET DOLORE MAGNA ALIQUA. PHARETRA VEL TURPIS NUNC EGET LOREM DOLOR SED VIVERRA IPSUM. LEO A DIAM SOLLICITUDIN TEMPOR ID EU NISL NUNC MI. EGESTAS CONGUE QUISQUE EGESTAS DIAM. NISI SCELERISQUE EU ULTRICES VITAE AUCTOR EU AUGUE UT LECTUS. RISUS NEC FEUGIAT IN FERMENTUM POSUERE URNA NEC. SED CRAS ORNARE ARCU DUI VIVAMUS ARCU FELIS BIBENDUM. IN FERMENTUM POSUERE URNA NEC TINCIDUNT. UT EU SEM INTEGER VITAE JUSTO EGET MAGNA FERMENTUM. VITAE NUNC SED VELIT DIGNISSIM. NAM ALIQUAM SEM ET TORTOR CONSEQUAT. LECTUS PROIN NIBH NISL CONDIMENTUM ID VENENATIS A CONDIMENTUM VITAE. IN CURSUS TURPIS MASSA TINCIDUNT DUI UT ORNARE LECTUS SIT. ARCU BIBENDUM AT VARIUS VEL PHARETRA VEL.'
ack                 = 0                         # Ultimo ack para msg do cliente, so atualizando se for maior

UDPServerSocket     = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))


# Envia resposta para cliente
def sendResponse(recSeq, recAck, address):
    global ack
    if (recAck >= ack):                                         # Encaixa o ACK no header
        ackStr = str(recSeq+messageSize).rjust(             # Se ACK da msg recebida for maior que armazenado,
                round(headerSize/2), '0')                   # servidor envia ACK para a mensagem recebida,
        ack = recAck                                
    else: ackStr = str(ack).rjust(round(headerSize/2), '0') # se nao, envia o ack armazenado (maior)
    seqStr = str(recSeq).rjust((round(headerSize/2)), '0')      # Encaixa o SEQ no header
    msg = str(msgFromServer[recSeq:recSeq + messageSize])       # Extrai proximo segmento da mensagem
    print("Enviado:{msg}")
    print("---------------------------")
    UDPServerSocket.sendto(str.encode(seqStr + ackStr + msg), address)  # Envia resposta para cliente


# Loop principal
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)     # Recebe msg do cliente (nao usa timeout)
    time.sleep(0.5)                                             # Sleep para simular diversos atrasos
    message = bytesAddressPair[0]                               # Extrai msg da tupla recebida
    address = bytesAddressPair[1]                               # Extrai informacoes do remetente da tupla
    print(f"Address Client:{format(address)}")
    print(f"Recebido:{format(message)}")
    recSeq = int(str(format(message))[2:2+round(headerSize/2)])             # Extrai SEQ da msg recebida
    recAck = int(str(format(message))[2+round(headerSize/2):2+headerSize])  # Extrai ACK da msg recebida
    sendResponse(recSeq, recAck, address)                            # Envia resposta
    


