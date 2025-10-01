import io
import socket
import shlex
from PIL import Image

def main():
    HOST = '127.0.0.1'
    PORT = 65432

    entrada_do_usuario = input("Digite o 'nome_arquivo.jpg' 'texto superior' 'texto inferior': ")
    argumentos = shlex.split(entrada_do_usuario)

    if len(argumentos) < 3:
        print("Erro: Uso: nome_arquivo.jpg 'texto superior' 'texto inferior'")
        return

    arquivo_imagem, texto_superior, texto_inferior = argumentos[0], argumentos[1], argumentos[2]

    mensagem = f"{arquivo_imagem}\n{texto_superior}\n{texto_inferior}"
    print(f"Enviando mensagem:\n{mensagem}")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5.0)
        sock.sendto(mensagem.encode(), (HOST, PORT))
        print("Mensagem enviada. Aguardando resposta...")

        try:
            data, _ = sock.recvfrom(2)
        except socket.timeout:
                print("Timeout: Nenhuma resposta do servidor")
                return
        total_segmentos = int.from_bytes(data, byteorder='big')
        print(f"Total de segmentos a receber: {total_segmentos}")
        
        #iniciar buffer de recebimento
        buffer = [None] * total_segmentos
        recebidos = 0 

        while recebidos < total_segmentos:
            try:
                data, _ = sock.recvfrom(2048)
                idx = int.from_bytes(data[:2], byteorder='big')
                payload = data[2:]

                if buffer[idx] is None:
                    buffer[idx] = payload
                    recebidos += 1
                    print(f"Recebido segmento {idx+1}/{total_segmentos} ({len(payload)} bytes)")
            except socket.timeout:
                print("Timeout: transmissão incompleta")
                break
            
        if recebidos == total_segmentos:
            dados_imagem = b"".join(buffer)
            try:
                img = Image.open(io.BytesIO(dados_imagem))
                img.show()
                img.save("output.jpg")
                print("Imagem salva como output.jpg!")
            except Exception as e:
                print(f"Erro ao processar imagem: {e}")
                with open("debug_data.bin", "wb") as f:
                    f.write(dados_imagem)
                print("Dados brutos salvos em debug_data.bin")
        else:   
            print("Imagem incompleta ou não recebida")



if __name__ == "__main__":
    main()
        
