import io
import socket
from PIL import Image


def main():
    HOST = '127.0.0.1'  # Endereço IP do servidor
    PORT = 65432        # Porta que o servidor está escutando

    #conexão com o servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f'Conectado ao servidor {HOST}:{PORT}')

        #recebendo dados do servidor
        data = b''
        while True:
            packet = s.recv(4096)
            if not packet:
                break
            data += packet
        print('Imagem recebida do servidor')  

    img = Image.open(io.BytesIO(data)) # convertendo bytes para imagem
    img.show() # exibindo a imagem
    img.save('output.jpg')
    print('Imagem salva como output.jpg')

if __name__ == "__main__":
    main()

