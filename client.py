
import socket
import io
import shlex
from PIL import Image

def main():
    HOST = '127.0.0.1'  # Endereço IP do servidor
    PORT = 65432        # Porta que o servidor está escutando


    entrada_do_usuario = input("Digite o 'nome_arquivo.jpg' 'texto superior' 'texto inferior': ")
    
    # Divide a string em uma lista de argumentos
    argumentos = shlex.split(entrada_do_usuario)

    # Verifica se o número de argumentos é o esperado
    if len(argumentos) < 3:
        print("Erro: Número inválido de argumentos.")
        print("Uso: nome_arquivo.jpg 'texto superior' 'texto inferior'")
        return

    # Extrai os argumentos para variáveis
    arquivo_imagem, texto_superior, texto_inferior = argumentos[0], argumentos[1], argumentos[2]
    
    # Constrói a mensagem a ser enviada
    mensagem = f'{arquivo_imagem}\n{texto_superior}\n{texto_inferior}\n'
    print(f'Enviando mensagem:\n{mensagem}')

    # Conexão com o servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f'Conectado ao servidor {HOST}:{PORT}')

            # **ENVIA A MENSAGEM ANTES DE RECEBER OS DADOS**
            s.sendall(mensagem.encode('utf-8'))

            # Recebendo dados do servidor
            data = b''
            while True:
                packet = s.recv(4096)
                if not packet:
                    break
                data += packet
            
            print('Imagem recebida do servidor') 

            # Processando os dados recebidos
            if data.startswith(b'ERRO:'):
                print(data.decode('utf-8'))
            else:
                img = Image.open(io.BytesIO(data)) # convertendo bytes para imagem
                img.show() # exibindo a imagem
                img.save('output.jpg')
                print('Imagem salva como output.jpg')

        except ConnectionRefusedError:
            print(f"Erro: Não foi possível conectar ao servidor em {HOST}:{PORT}.")
            print("Certifique-se de que o servidor está em execução.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            print(' ')

if __name__ == "__main__":
    main()


