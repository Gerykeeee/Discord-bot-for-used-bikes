# GSX-R Hunter Discord Bot 🏍️

*For English description, please scroll down.*

## 🇭🇺 Magyar

A **GSX-R Hunter** egy Discord bot, amely a magyar [Képesmotor](https://www.kepesmotor.hu/) weboldalt figyeli megadott (2003-2006-os) Suzuki GSX-R sportmotorok hirdetései után. Automatikusan lekéri a friss hirdetéseket, elemzi azok szövegét, eldönti róluk, hogy rendelkeznek-e érvényes okmányokkal (utcai használatra alkalmasak-e), és az eredményeket Discord csatornákra továbbítja beágyazott (embed) üzenetek formájában.

### ✨ Funkciók
- **Automatikus Scraping:** Óránként lekérdezi a Képesmotor hirdetéseit.
- **Szöveg Analízis:** Kulcsszavak alapján szétválogatja a magyar okmányos és a pálya/hiányos papírral rendelkező motorokat.
- **Adatbázis (SQLite):** Helyi adatbázisban tárolja a már megtalált hirdetéseket a duplikációk elkerülése végett.
- **Okos Kategórizálás:** Két külön Discord csatornára tud posztolni: az egyikbe minden találatot, a másikba csak az okmányokkal rendelkező utcai motorokat.
- **Törölt Hirdetések Figyelése:** A `!frissit` paranccsal ellenőrzi az adatbázisban lévő linkeket, és frissíti a státuszukat, ha időközben eladták/törölték őket.

### 🚀 Telepítés és Futtatás
1. Klónozd a repót: `git clone https://github.com/FELHASZNÁLÓNEVED/REPO-NEVE.git`
2. Telepítsd a szükséges Python csomagokat:
   `pip install discord.py requests beautifulsoup4`
3. A kód elején lévő konfigurációs részben írd át a következőket a saját adataidra (Figyelem: Ezt a fájlt ne tedd publikussá a tokeneddel!):
   - `BOT_TOKEN`
   - `CHANNEL_ALL_ID`
   - `CHANNEL_STREET_ID`
4. Futtasd a botot: `python bot.py` (vagy a fájlod neve)

---

## 🇬🇧 English

**GSX-R Hunter** is a Discord bot designed to scrape the Hungarian motorcycle classifieds website [Képesmotor](https://www.kepesmotor.hu/). It specifically searches for Suzuki GSX-R sports bikes (made between 2003 and 2006). The bot automatically fetches new listings, analyzes their descriptions to determine if they are street-legal (have valid Hungarian paperwork), and sends the parsed results to specific Discord channels.

### ✨ Features
- **Automated Web Scraping:** Checks for new listings every 60 minutes.
- **Text Analysis:** Uses keyword filtering to distinguish between street-legal bikes and track/paperless ones.
- **SQLite Database:** Stores already processed listings locally to prevent duplicate Discord messages.
- **Smart Routing:** Forwards all listings to a general channel, while exclusively sending street-legal bikes to a dedicated channel.
- **Sold/Deleted Listing Tracker:** The `!frissit` (update) command verifies existing database links and marks them as sold/deleted if the URL returns a 404 or inactive status.

### 🚀 Installation & Setup
1. Clone the repository: `git clone https://github.com/YOURUSERNAME/YOUR-REPO-NAME.git`
2. Install the required Python dependencies:
   `pip install discord.py requests beautifulsoup4`
3. Open the code and fill in the configuration variables with your own credentials (Warning: Never commit your real bot token to a public repository!):
   - `BOT_TOKEN`
   - `CHANNEL_ALL_ID`
   - `CHANNEL_STREET_ID`
4. Run the script: `python bot.py` (or whatever you named the file)
