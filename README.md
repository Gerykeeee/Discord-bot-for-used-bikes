## Universal Scraper Discord Bot 🤖

For English description, please scroll down.

### 🇭🇺 Magyar

A **Universal Scraper** egy Discord bot, amely megadott weboldalakat figyel előre beállított paraméterek (kívánt termékek, cikkek, hirdetések) alapján. Automatikusan lekéri a friss találatokat, elemzi azok szövegét és adatait, majd a beállított szűrők alapján kategóriákba sorolja őket. Az eredményeket dedikált Discord csatornákra továbbítja átlátható, beágyazott (embed) üzenetek formájában.

**✨ Funkciók**

*   **Automatikus Scraping:** Rendszeres időközönként lekérdezi a céloldalak új találatait.
*   **Szöveg Analízis:** Kulcsszavak és paraméterek alapján szűri és kategóriákba rendezi a találatokat (pl. állapot, ár, vagy specifikus tulajdonságok alapján).
*   **Adatbázis (SQLite):** Helyi adatbázisban tárolja a már feldolgozott elemeket a Discord üzenetek duplikációjának elkerülése végett.
*   **Okos Kategórizálás:** Külön Discord csatornákra tud posztolni a szűrési feltételek alapján (pl. minden találat egy általános csatornába, míg a kiemelt vagy specifikus feltételeknek megfelelőek egy másikba).
*   **Törölt Elemek Figyelése:** A `!frissit` paranccsal ellenőrzi az adatbázisban lévő linkeket, és frissíti a státuszukat, ha időközben eltávolították vagy eladták őket.

**🚀 Telepítés és Futtatás**

1.  **Klónozd a repót:** `git clone https://github.com/FELHASZNÁLÓNEVED/REPO-NEVE.git`
2.  **Telepítsd a szükséges Python csomagokat:** `pip install discord.py requests beautifulsoup4`
3.  **Konfiguráció:** A kód elején lévő konfigurációs részben írd át a következőket a saját adataidra *(Figyelem: Ezt a fájlt ne tedd publikussá a tokeneddel!)*:
    *   `BOT_TOKEN`
    *   `CHANNEL_ALL_ID`
    *   `CHANNEL_FILTERED_ID`
4.  **Futtasd a botot:** `python bot.py` (vagy a fájlod pontos neve)

---

### 🇬🇧 English

**Universal Scraper** is a Discord bot designed to monitor specified websites for desired products, articles, or listings based on predefined parameters. The bot automatically fetches new items, analyzes their descriptions or content, categorizes them based on user-defined criteria, and sends the parsed results to specific Discord channels using formatted embed messages.

**✨ Features**

*   **Automated Web Scraping:** Checks the target websites for new items at configurable intervals.
*   **Text Analysis:** Uses keyword filtering to categorize and filter results (e.g., by condition, specific features, availability, or pricing).
*   **SQLite Database:** Stores already processed items locally to prevent duplicate Discord messages.
*   **Smart Routing:** Forwards items to different channels based on the filtering rules (e.g., sending all results to a general channel, while exclusively sending highly matched items to a dedicated channel).
*   **Removed/Sold Item Tracker:** The `!frissit` (update) command verifies existing database links and marks them as unavailable if the URL returns a 404 or inactive status.

**🚀 Installation & Setup**

1.  **Clone the repository:** `git clone https://github.com/YOURUSERNAME/YOUR-REPO-NAME.git`
2.  **Install the required Python dependencies:** `pip install discord.py requests beautifulsoup4`
3.  **Configuration:** Open the code and fill in the configuration variables with your own credentials *(Warning: Never commit your real bot token to a public repository!)*:
    *   `BOT_TOKEN`
    *   `CHANNEL_ALL_ID`
    *   `CHANNEL_FILTERED_ID`
4.  **Run the script:** `python bot.py` (or whatever you named the file)
