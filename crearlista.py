import yt_dlp
import re
import os
import time

# ============== BANNER NUEVO ==============
print("""
╭━╮╱╱╱╱╱╱╱╱╱╭┳┳━┳╮╱╱╱╱
┃╭╋┳┳━┳━╮╭┳╮┃┣┫━┫╰┳━╮╱
┃╰┫╭┫┻┫╋╰┫╭╯┃┃┣━┃╭┫╋╰╮
╰━┻╯╰━┻━━┻╯╱╰┻┻━┻━┻━━╯

🄱🅈 🅂🄰🄼🄰🄴🄻 
""")
print("\033[1;35mHerramienta para crear listas IPTV\033[m\n")
time.sleep(1)

# Ruta de guardado
RUTA_LISTA = '/sdcard/descargas/lista.m3u'


def remover_acentos_e_emojis(texto):
    """Limpia tildes, emojis y caracteres especiales sin borrar espacios"""
    if not texto:
        return "Sin_Titulo"
    
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
    
    texto = re.sub(r'[^\w\s\-\(\)\[\]]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto if texto else "Sin_Titulo"


def obtener_enlace_video(video_url):
    """Extrae el enlace reproducible de yt-dlp con manejo de errores"""
    
    ydl_opts = {
        'format': 'best',
        'quiet': False,
        'no_warnings': False,
        'extract_flat': False,
    }
    
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
            
            enlace = None
            enlace = next((f['manifest_url'] for f in info.get('formats', []) 
                          if f.get('manifest_url', '').endswith('.m3u8')), None)
            
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


def guardar_en_lista(titulo, enlace):
    """Guarda el enlace en formato M3U en /sdcard/descargas/"""
    try:
        os.makedirs(os.path.dirname(RUTA_LISTA), exist_ok=True)
        with open(RUTA_LISTA, 'a', encoding='utf-8') as f:
            f.write(f"#EXTINF:-1,{titulo}\n")
            f.write(f"{enlace}\n")
        print(f"💾 Guardado en: {RUTA_LISTA}")
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
    print(f"📌 Los archivos se guardarán en: {RUTA_LISTA}\n")
    
    while True:
        entrada = input("\n🔗 Ingresa enlace o comando: ").strip()
        
        if entrada.lower() in ['salir', 'exit', 'q']:
            print("\n👋 ¡Lista lista! Hasta luego")
            break
        
        if entrada.lower() == 'ayuda':
            mostrar_ayuda()
            continue
        
        if entrada.lower() == 'lista':
            if os.path.exists(RUTA_LISTA):
                with open(RUTA_LISTA, 'r', encoding='utf-8') as f:
                    lineas = f.readlines()
                    videos = len([l for l in lineas if l.startswith('#EXTINF')])
                    print(f"📋 Tu lista tiene: {videos} videos")
            else:
                print("📋 Aún no has guardado nada")
            continue
        
        if entrada.lower() == 'limpiar':
            confirmar = input("⚠️ ¿Borrar todo? (s/n): ").lower()
            if confirmar == 's':
                open(RUTA_LISTA, 'w').close()
                print("🗑️ Lista vaciada")
            continue
        
        if entrada.startswith(('http://', 'https://')):
            titulo, enlace = obtener_enlace_video(entrada)
            if titulo and enlace:
                guardar_en_lista(titulo, enlace)
        else:
            print("❌ No reconozco eso. Escribe 'ayuda' para ver opciones")


if __name__ == "__main__":
    main()
