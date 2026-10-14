import yt_dlp
import re
import os
import pyfiglet
from rich.console import Console
from rich.text import Text
import time

console = Console()
esp = ' '

# Banner
banner1 = pyfiglet.figlet_format(f'{esp*2}C R I A R', font='slant')
banner2 = pyfiglet.figlet_format(f'{esp*2}L I S T A', font='slant')
banner3 = pyfiglet.figlet_format(f'{esp*3}I P T V', font='slant')

console.print(f'[blue]{banner1}[/blue]')
console.print(f'[blue]{banner2}[/blue]')
console.print(f'[cyan]{banner3}[/cyan]')
print('\033[1;44mHecho por @DarkJVPN - Versión mejorada\033[m\n')
time.sleep(1)


def remover_acentos_e_emojis(texto):
    """Limpia tildes, emojis y caracteres especiales sin borrar espacios"""
    if not texto:
        return "Sin_Titulo"
    
    # Reemplazar acentos
    reemplazos = {
        r'[áàâãä]': 'a', r'[ÁÀÂÃÄ]': 'A',
        r'[éèêë]': 'e', r'[ÉÈÊË]': 'E',
        r'[íìîï]': 'i', r'[ÍÌÎÏ]': 'I',
        r'[óòôõö]': 'o', r'[ÓÒÔÕÖ]': 'O',
        r'[úùûü]': 'u', r'[ÚÙÛÜ]': 'U',
        r'[ç]': 'c', r'[Ç]': 'C',
    }
    for patron, reemplazo in reemplazos.items():
        texto = re.sub(patron, reemplazo, texto)
    
    # Eliminar emojis y símbolos raros PERO mantener espacios
    texto = re.sub(r'[^\w\s\-\(\)\[\]]', '', texto)
    # Eliminar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto if texto else "Sin_Titulo"


def obtener_enlace_video(video_url):
    """Extrae el enlace reproducible de yt-dlp con manejo de errores"""
    
    ydl_opts = {
        'format': 'best',  # Cambiado: obtiene el mejor formato disponible
        'quiet': False,
        'no_warnings': False,
        'extract_flat': False,
    }
    
    # Si existe cookies.txt, usarlo (ayuda con Dailymotion)
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'
        print("✅ Archivo de cookies detectado y activado")
    
    try:
        print(f"\n🔍 Analizando: {video_url}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            if not info:
                print("❌ No se pudo obtener información del video")
                return None, None
            
            titulo = info.get('title', 'Sin Título')
            titulo_limpio = remover_acentos_e_emojis(titulo)
            
            # Buscar el mejor enlace reproducible
            enlace = None
            
            # 1. Buscar m3u8 primero
            enlace = next((f['manifest_url'] for f in info.get('formats', []) 
                          if f.get('manifest_url', '').endswith('.m3u8')), None)
            
            # 2. Si no hay m3u8, usar el enlace directo del mejor formato
            if not enlace:
                mejor_formato = info.get('url') or info.get('formats', [{}])[0].get('url')
                enlace = mejor_formato
            
            if enlace:
                print(f"✅ Video encontrado: {titulo_limpio}")
                return titulo_limpio, enlace
            else:
                print("❌ No se encontró un enlace reproducible")
                return None, None
    
    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ Error de descarga: {str(e)[:100]}...")
        print("💡 Sugerencia: Actualiza yt-dlp con: yt-dlp -U")
        return None, None
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return None, None


def guardar_en_lista(titulo, enlace, archivo='lista.m3u'):
    """Guarda el enlace en formato M3U con codificación correcta"""
    try:
        with open(archivo, 'a', encoding='utf-8') as f:
            f.write(f"#EXTINF:-1,{titulo}\n")
            f.write(f"{enlace}\n")
        print(f"💾 Guardado en: {archivo}")
        return True
    except Exception as e:
        print(f"❌ Error al guardar: {e}")
        return False


def mostrar_ayuda():
    print("""
╔══════════════════════════════════════════╗
║      COMANDOS DISPONIBLES                 ║
╠══════════════════════════════════════════╣
║  pegar enlace → Agregar video            ║
║  lista        → Ver cuántos tienes       ║
║  limpiar      → Borrar la lista actual   ║
║  salir        → Cerrar el programa       ║
╚══════════════════════════════════════════╝
    """)


def main():
    print("📌 Ingresa los enlaces de YouTube, Dailymotion, etc.\n")
    
    while True:
        entrada = input("\n🔗 Ingresa enlace o comando: ").strip()
        
        if entrada.lower() in ['salir', 'exit', 'q']:
            print("\n👋 ¡Lista lista! Hasta luego")
            break
        
        if entrada.lower() == 'ayuda':
            mostrar_ayuda()
            continue
        
        if entrada.lower() == 'lista':
            if os.path.exists('lista.m3u'):
                with open('lista.m3u', 'r', encoding='utf-8') as f:
                    lineas = f.readlines()
                    videos = len([l for l in lineas if l.startswith('#EXTINF')])
                    print(f"📋 Tu lista tiene: {videos} videos")
            else:
                print("📋 Aún no has guardado nada")
            continue
        
        if entrada.lower() == 'limpiar':
            confirmar = input("⚠️ ¿Borrar todo? (s/n): ").lower()
            if confirmar == 's':
                open('lista.m3u', 'w').close()
                print("🗑️ Lista vaciada")
            continue
        
        # Procesar como enlace
        if entrada.startswith(('http://', 'https://')):
            titulo, enlace = obtener_enlace_video(entrada)
            if titulo and enlace:
                guardar_en_lista(titulo, enlace)
        else:
            print("❌ No reconozco eso. Escribe 'ayuda' para ver opciones")


if __name__ == "__main__":
    main()
