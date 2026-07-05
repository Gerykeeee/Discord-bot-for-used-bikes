import discord
from discord.ext import commands, tasks
import sqlite3
import requests
from bs4 import BeautifulSoup
import asyncio
import re

# ==========================================
# KONFIGURÁCIÓ
# ==========================================
BOT_TOKEN = 'Saját Discord Developer Tokened' 
CHANNEL_ALL_ID = # ide jön a csatorna id
CHANNEL_STREET_ID = # ide jön a csatorna id

SEARCH_URL = "https://www.kepesmotor.hu/suzuki-sportmotor/?made_year_min=2003&made_year_max=2006"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# ==========================================
# ADATBÁZIS INICIALIZÁLÁS
# ==========================================
def init_db():
    conn = sqlite3.connect('gsxr_vadon.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS motorok (
            id TEXT PRIMARY KEY,
            cim TEXT,
            link TEXT,
            utcai INTEGER,
            statusz TEXT DEFAULT 'aktiv'
        )
    ''')
    conn.commit()
    conn.close()

# ==========================================
# SCRAPER LOGIKA
# ==========================================
def is_street_legal(cim, leiras):
    teljes_szoveg = f"{cim} {leiras}".lower()
    kizaro_szavak = ["okmányok nélkül", "papírok nélkül", "külföldi"]
    for szo in kizaro_szavak:
        if szo in teljes_szoveg:
            return False
            
    elfogado_szavak = ["érvényes okmány", "magyar okmány", "forgalmi", "ideiglenesen kivonva", "rendszám", "műszaki"]
    for szo in elfogado_szavak:
        if szo in teljes_szoveg:
            return True
    return False

def scrape_new_motors():
    try:
        response = requests.get(SEARCH_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Hiba a Képesmotor elérésekor: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    hirdetes_linkek = soup.find_all('a', href=True)
    
    conn = sqlite3.connect('gsxr_vadon.db')
    cursor = conn.cursor()
    
    uj_motorok = []
    feldolgozott_idek = set()
    
    for link_elem in hirdetes_linkek:
        href = link_elem['href']
        
        # Reklámok szűrése
        if "/p" in href and "-sportmotor/" in href:
            hirdetes_id = href.split('/p')[-1]
            
            if hirdetes_id in feldolgozott_idek:
                continue
            feldolgozott_idek.add(hirdetes_id)
            
            
            cursor.execute("SELECT id FROM motorok WHERE id = ?", (hirdetes_id,))
            
            if cursor.fetchone() is None:
                cim = link_elem.text.strip() or link_elem.get('title', 'Suzuki GSX-R')
                teljes_link = f"https://www.kepesmotor.hu{href}"
                
                
                try:
                    ad_resp = requests.get(teljes_link, headers=HEADERS, timeout=10)
                    ad_soup = BeautifulSoup(ad_resp.text, 'html.parser')
                    
                    
                    kep_meta = ad_soup.find('meta', property='og:image')
                    kep_url = kep_meta['content'] if kep_meta else None
                    
                    
                    desc_meta = ad_soup.find('meta', property='og:description')
                    teljes_leiras = desc_meta['content'] if desc_meta else "Nincs megadva leírás."
                    
                    
                    ar_elem = ad_soup.find(string=re.compile(r'Ft$'))
                    ar = ar_elem.strip() if ar_elem else "Nincs megadott ár"
                    
                    
                    evjarat_match = re.search(r'(200[3-6])', cim + ad_soup.text)
                    evjarat = evjarat_match.group(1) if evjarat_match else "Ismeretlen"
                    
                    
                    utcai = 1 if is_street_legal(cim, ad_soup.text) else 0
                    
                except Exception as e:
                    print(f"Hiba a részletek letöltésekor ({teljes_link}): {e}")
                    continue 

                # Mentés adatbázisba
                cursor.execute(
                    "INSERT INTO motorok (id, cim, link, utcai) VALUES (?, ?, ?, ?)",
                    (hirdetes_id, cim, teljes_link, utcai)
                )
                
                uj_motorok.append({
                    'id': hirdetes_id,
                    'cim': cim,
                    'link': teljes_link,
                    'utcai': bool(utcai),
                    'ar': ar,
                    'evjarat': evjarat,
                    'leiras': teljes_leiras,
                    'kep': kep_url
                })
                
    conn.commit()
    conn.close()
    return uj_motorok

# ==========================================
# DISCORD BOT BEÁLLÍTÁSOK
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    init_db()
    print(f'Sikeresen bejelentkezve mint {bot.user}')
    if not motor_figyelo.is_running():
        motor_figyelo.start()


@tasks.loop(minutes=60)
async def motor_figyelo():
    print("Képesmotor ellenőrzése...")
    uj_talalatok = scrape_new_motors()
    
    if not uj_talalatok:
        return
        
    channel_all = bot.get_channel(CHANNEL_ALL_ID)
    channel_street = bot.get_channel(CHANNEL_STREET_ID)
    
    for motor in uj_talalatok:
        rovid_leiras = motor['leiras'][:200] + "..." if len(motor['leiras']) > 200 else motor['leiras']
        
        embed = discord.Embed(
            title=f"{motor['cim']} ({motor['evjarat']})", 
            url=motor['link'], 
            description=rovid_leiras,
            color=0x00ff00 if motor['utcai'] else 0xff9900
        )
        
        embed.add_field(name="Ár", value=motor['ar'], inline=True)
        embed.add_field(name="Állapot", value="✅ Magyar okmányos" if motor['utcai'] else "❓ Pálya / Hiányos", inline=True)
        
        if motor['kep']:
            embed.set_image(url=motor['kep'])
        
        if channel_all:
            await channel_all.send(embed=embed)
            
        if motor['utcai'] and channel_street:
            await channel_street.send(embed=embed)

# ==========================================
# !FRISSIT PARANCS 
# ==========================================
@bot.command()
async def frissit(ctx):
    await ctx.send("🔄 Keresem az eladott vagy törölt hirdetéseket a háttérben...")
    
    conn = sqlite3.connect('gsxr_vadon.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, link FROM motorok WHERE statusz = 'aktiv'")
    aktiv_motorok = cursor.fetchall()
    
    eladott_szamlalo = 0
    
    for hirdetes_id, link in aktiv_motorok:
        try:
            await asyncio.sleep(1) 
            resp = requests.get(link, headers=HEADERS, timeout=10)
            
            if resp.status_code == 404 or "A hirdetés már nem aktív" in resp.text:
                cursor.execute("UPDATE motorok SET statusz = 'eladva' WHERE id = ?", (hirdetes_id,))
                eladott_szamlalo += 1
        except Exception as e:
            print(f"Hiba a(z) {link} ellenőrzésekor: {e}")
            
    conn.commit()
    conn.close()
    
    await ctx.send(f"✅ Frissítés kész! **{eladott_szamlalo}** motor lett eladva / levéve az oldalról az adatbázis szerint.")

if __name__ == "__main__":
    init_db()
    bot.run(BOT_TOKEN)
