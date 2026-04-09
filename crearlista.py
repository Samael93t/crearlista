import yt_dlp
import re
import os
import pyfiglet
import rich
import time

esp = ' '
banner1 = pyfiglet.figlet_format(f'{esp*2}C R I A R', font='slant')
banner2 = pyfiglet.figlet_format(f'{esp*2}L I S T A', font='slant')
banner3 = pyfiglet.figlet_format(f'{esp*3}I P T V', font='slant')
rich.print(f'[blue]{banner1}[/blue]')
rich.print(f'[blue]{banner2}[/blue]')
rich.print(f'[silver]{banner3}[/silver]')
print('\033[1;44mFeito por @DarkJVPN\033[m\n\n\n')
time.sleep(1)


def remover_acentos_e_emojis(texto):
    
    texto = re.sub(r'[^\w\s]', '', texto)
    
    
    texto = re.sub(r'[áàâãä]', 'a', texto)
    texto = re.sub(r'[ÁÀÂÃÄ]', 'A', texto)
    texto = re.sub(r'[éèêë]', 'e', texto)
    texto = re.sub(r'[ÉÈÊË]', 'E', texto)
    texto = re.sub(r'[íìîï]', 'i', texto)
    texto = re.sub(r'[ÍÌÎÏ]', 'I', texto)
    texto = re.sub(r'[óòôõö]', 'o', texto)
    texto = re.sub(r'[ÓÒÔÕÖ]', 'O', texto)
    texto = re.sub(r'[úùûü]', 'u', texto)
    texto = re.sub(r'[ÚÙÛÜ]', 'U', texto)
    texto = re.sub(r'[ç]', 'c', texto)
    texto = re.sub(r'[Ç]', 'C', texto)
    
    return texto

def obter_video_url(video_url):
    ydl_opts = {
        'cookiefile': 'cookies.txt',
        'format': 'bestvideo+bestaudio/best',  
        'noplaylist': True,
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)

            video_title = info.get('title', 'Título Desconhecido')
            video_title = remover_acentos_e_emojis(video_title)  

            m3u8_url = next((format['manifest_url'] for format in info['formats']
                             if 'manifest_url' in format and '.m3u8' in format['manifest_url']), None)

            if m3u8_url:
                print(f"Vídeo Encontrado: {video_title}")
                return video_title, m3u8_url

            print("Nenhum link de vídeo .m3u8 encontrado no 'manifest_url'.")
            return None, None

        except Exception as e:
            print(f"Erro: {e}")
            return None, None

def salvar_playlist(video_title, video_url):
    with open('playlist.m3u8', 'a') as f:
        f.write(f"#EXTINF:-1,{video_title}\n")
        f.write(f"{video_url}\n")
        print(f"Playlist salva como 'playlist.m3u8'.")

def main():
    while True:
        video_url = input("Digite o link do vídeo do YouTube (ou 'sair' para sair): ")
        if video_url.lower() == 'sair':
            break
        video_title, video_url = obter_video_url(video_url)
        if video_title and video_url:  
            salvar_playlist(video_title, video_url)

if __name__ == "__main__":
    main()
