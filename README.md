# Artemis II Trajectory Simulation (`artemis-pymulation`)

Trójwymiarowa, interaktywna symulacja trajektorii lotu misji kosmicznej Artemis II, zrealizowana w języku Python przy użyciu biblioteki **VPython** na potrzeby projektu z fizyki.

Symulacja pozwala na badanie mechaniki nieba oraz planowanie i analizę **trajektorii swobodnego powrotu** (ang. *free return trajectory*) dla statku kosmicznego podróżującego z Ziemi w okolice Księżyca i z powrotem.

---

## 🚀 Główne Funkcje Symulacji

1. **Interaktywna Wizualizacja 3D w Czasie Rzeczywistym:**
   - Realistycznie wyskalowane modele Ziemi (wraz z nałożoną teksturą geograficzną), Księżyca oraz statku kosmicznego.
   - Dynamicznie generowany, trójwymiarowy ślad trajektorii lotu statku (kolor pomarańczowy) oraz orbita Księżyca (szara).
   - Pełna kontrola kamery 3D (obracanie prawym przyciskiem myszy, przybliżanie kółkiem/dwoma palcami).

2. **Zaawansowany Panel Sterowania parametrami początkowymi:**
   - **Prędkość ucieczki (Exit velocity):** Regulacja dodatkowej prędkości początkowej manewru TLI (*Trans-Lunar Injection*) dodawanej do prędkości na orbicie parkingowej (domyślnie $+3150 \text{ m/s}$).
   - **Kąt startu misji (Mission start angle):** Położenie statku kosmicznego na kołowej orbicie parkingowej wokół Ziemi w momencie odpalenia silników TLI (domyślnie $120^\circ$).
   - **Kąt położenia Księżyca (Moon position angle):** Ustalenie fazy (pozycji) Księżyca na orbicie w chwili rozpoczęcia misji (domyślnie $244^\circ$).

3. **Dynamiczna Kontrola Czasu i Stanu Symulacji:**
   - **Launch Mission / Launched:** Uruchomienie obliczeń fizycznych i start statku z orbity parkingowej.
   - **Pause / Resume:** Wstrzymanie i wznawianie symulacji w dowolnym momencie.
   - **Reset:** Powrót do parametrów początkowych, wyczyszczenie śladu i przygotowanie do nowego startu.
   - **Faster / Slower:** Skalowanie kroku czasu rzeczywistego (przyspieszanie i zwalnianie upływu czasu w symulacji).

4. **HUD Telemetrii w Czasie Rzeczywistym (Dark Mode):**
   - **Status misji:** `AWAITING LAUNCH`, `IN FLIGHT`, `PAUSED`, `MISSION COMPLETE`.
   - **Czas misji (MET):** *Mission Elapsed Time* wyrażony w dniach, godzinach, minutach i sekundach.
   - **Parametry orbitalne względem Ziemi:** Wysokość (Altitude) w km i prędkość (Velocity) w km/s.
   - **Parametry orbitalne względem Księżyca:** Wysokość w km i prędkość w km/s.

---

## 📐 Podstawy Fizyczne i Model Numeryczny

Symulacja bazuje na **uproszczonym problemie trzech ciał** (Ziemia, Księżyc, statek kosmiczny), w którym masa statku kosmicznego ($m$) jest zaniedbywalnie mała w porównaniu z masami Ziemi ($M_E$) i Księżyca ($M_M$). Dzięki temu statek nie wpływa grawitacyjnie na orbity ciał niebieskich, a same ciała niebieskie oddziałują tylko ze sobą i ze statkiem.

### 1. Równania Ruchu

Środek układu współrzędnych umieszczony jest w środku Ziemi ($\vec{r}_{earth} = \vec{0}$).

- **Ruch statku kosmicznego:**
  Statek podlega grawitacji Ziemi i Księżyca zgodnie z równaniem przyspieszenia:
  $$\vec{a}_{ship} = - \frac{G M_E}{|\vec{r}_{se}|^3} \vec{r}_{se} + \frac{G M_M}{|\vec{r}_{sm}|^3} \vec{r}_{sm}$$

  gdzie:
  - $G = 6.674 \times 10^{-11} \text{ m}^3 \text{ kg}^{-1} \text{ s}^{-2}$ – stała grawitacji,
  - $M_E = 5.972 \times 10^{24} \text{ kg}$ – masa Ziemi,
  - $M_M = 7.342 \times 10^{22} \text{ kg}$ – masa Księżyca,
  - $\vec{r}_{se} = \vec{r}_{ship} - \vec{r}_{earth} = \vec{r}_{ship}$ – wektor położenia statku względem Ziemi,
  - $\vec{r}_{sm} = \vec{r}_{ship} - \vec{r}_{moon}$ – wektor położenia statku względem Księżyca.

- **Ruch Księżyca:**
  Księżyc porusza się po stabilnej orbicie kołowej o promieniu $d_{EM} = 384\ 400 \text{ km}$ wokół Ziemi z prędkością orbitalną $v_M \approx 1022 \text{ m/s}$, a jego przyspieszenie opisuje wzór:
  $$\vec{a}_{moon} = - \frac{G M_E}{|\vec{r}_{moon}|^3} \vec{r}_{moon}$$

### 2. Metody Integracji Numerycznej

Do numerycznego rozwiązywania równań różniczkowych zwyczajnych drugiego rzędu zastosowano dwie różne metody całkowania:

- **Dla statku kosmicznego – Rungego-Kutty IV rzędu (RK4):**
  Zaimplementowana w funkcji [rk4](file:///home/mzych/PycharmProjects/artemis-pymulation/src/physics.py#L24). Metoda RK4 cechuje się błędem lokalnym rzędu $\mathcal{O}(h^5)$ i globalnym $\mathcal{O}(h^4)$. Jest to kluczowe podczas bliskich przelotów obok Księżyca (asysta grawitacyjna), gdzie pole grawitacyjne zmienia się bardzo dynamicznie, a zwykła metoda Eulera prowadziłaby do ogromnych błędów skumulowanych (np. niefizycznego wystrzelenia statku z układu lub zderzenia).
  Dla każdego kroku czasowego $h$ obliczane są cztery współczynniki nachylenia pola prędkości i przyspieszenia:
  - $\vec{k}_{1v} = \vec{a}(\vec{r}_n, \vec{r}_{moon})$, $\quad \vec{k}_{1p} = \vec{v}_n$
  - $\vec{k}_{2v} = \vec{a}(\vec{r}_n + 0.5 h \vec{k}_{1p}, \vec{r}_{moon})$, $\quad \vec{k}_{2p} = \vec{v}_n + 0.5 h \vec{k}_{1v}$
  - $\vec{k}_{3v} = \vec{a}(\vec{r}_n + 0.5 h \vec{k}_{2p}, \vec{r}_{moon})$, $\quad \vec{k}_{3p} = \vec{v}_n + 0.5 h \vec{k}_{2v}$
  - $\vec{k}_{4v} = \vec{a}(\vec{r}_n + h \vec{k}_{3p}, \vec{r}_{moon})$, $\quad \vec{k}_{4p} = \vec{v}_n + h \vec{k}_{3v}$
  - Nowa pozycja: $\vec{r}_{n+1} = \vec{r}_n + \frac{h}{6}(\vec{k}_{1p} + 2\vec{k}_{2p} + 2\vec{k}_{3p} + \vec{k}_{4p})$
  - Nowa prędkość: $\vec{v}_{n+1} = \vec{v}_n + \frac{h}{6}(\vec{k}_{1v} + 2\vec{k}_{2v} + 2\vec{k}_{3v} + \vec{k}_{4v})$

- **Dla Księżyca – Euler-Cromer:**
  Zaimplementowana w funkcji [euler_moon](file:///home/mzych/PycharmProjects/artemis-pymulation/src/physics.py#L46). Ponieważ orbita Księżyca jest idealnie kołowa i nie wpływa na nią lekki statek, do jej opisu wystarczy metoda Eulera-Cromera (pół-niejawna metoda Eulera), która zachowuje energię mechaniczną układu (jest integratorem symplektycznym):
  - $\vec{v}_{moon, n+1} = \vec{v}_{moon, n} + \vec{a}_{moon}(\vec{r}_{moon, n}) \cdot h$
  - $\vec{r}_{moon, n+1} = \vec{r}_{moon, n} + \vec{v}_{moon, n+1} \cdot h$

---

## 🛠️ Struktura Projektu i Moduły

Kod źródłowy projektu znajduje się w katalogu `src` i jest podzielony na czytelne, wyspecjalizowane moduły:

- **[src/config.py](file:///home/mzych/PycharmProjects/artemis-pymulation/src/config.py):** Definiuje stałe fizyczne (masy ciał, promienie orbitalne), parametry początkowe (wysokość orbity parkingowej $185\text{ km}$, domyślne kąty), a także stałe wizualne (skalowanie ciał do wyświetlania w 3D, prędkości początkowe, krok czasowy integracji `DT = 30` sekund).
- **[src/physics.py](file:///home/mzych/PycharmProjects/artemis-pymulation/src/physics.py):** Zawiera funkcje obliczające przyspieszenia grawitacyjne ([accel_ship](file:///home/mzych/PycharmProjects/artemis-pymulation/src/physics.py#L6) oraz [accel_moon](file:///home/mzych/PycharmProjects/artemis-pymulation/src/physics.py#L16)) oraz solvery różniczkowe ([rk4](file:///home/mzych/PycharmProjects/artemis-pymulation/src/physics.py#L24) i [euler_moon](file:///home/mzych/PycharmProjects/artemis-pymulation/src/physics.py#L46)).
- **[src/simulation.py](file:///home/mzych/PycharmProjects/artemis-pymulation/src/simulation.py):** Klasa [Simulation](file:///home/mzych/PycharmProjects/artemis-pymulation/src/simulation.py#L11) zarządza stanem symulacji (położenie i prędkość statku i Księżyca), wykonuje kroki fizyczne ([step](file:///home/mzych/PycharmProjects/artemis-pymulation/src/simulation.py#L46)), sprawdza warunki zakończenia misji ([check_termination_conditions](file:///home/mzych/PycharmProjects/artemis-pymulation/src/simulation.py#L59) – np. ponowne wejście w atmosferę Ziemi lub przekroczenie limitu 13 dni) oraz agreguje dane do telemetrii ([get_telemetry](file:///home/mzych/PycharmProjects/artemis-pymulation/src/simulation.py#L67)).
- **[src/scene.py](file:///home/mzych/PycharmProjects/artemis-pymulation/src/scene.py):** Odpowiada za konfigurację sceny 3D biblioteki VPython ([setup_scene](file:///home/mzych/PycharmProjects/artemis-pymulation/src/scene.py#L11)) – w tym ustawienia kamery – oraz generowanie obiektów 3D reprezentujących Ziemię ([setup_earth](file:///home/mzych/PycharmProjects/artemis-pymulation/src/scene.py#L30)), Księżyc ([setup_moon](file:///home/mzych/PycharmProjects/artemis-pymulation/src/scene.py#L53)) i statek kosmiczny wraz z parametrami śladu orbitalnego ([setup_ship](file:///home/mzych/PycharmProjects/artemis-pymulation/src/scene.py#L80)).
- **[src/controls.py](file:///home/mzych/PycharmProjects/artemis-pymulation/src/controls.py):** Klasa [Controls](file:///home/mzych/PycharmProjects/artemis-pymulation/src/controls.py#L6) obsługuje callbacki GUI (obsługa ruchów suwaków parametrów początkowych, zmiana statusów przycisków, przyspieszanie i spowalnianie symulacji).
- **[src/styles.py](file:///home/mzych/PycharmProjects/artemis-pymulation/src/styles.py):** Definiuje arkusze CSS i kod JavaScript wstrzykiwane bezpośrednio do okna VPython, co umożliwia spersonalizowanie układu graficznego oraz stworzenie nowoczesnego HUD-u w stylu "dark mode".
- **[src/telemetry.py](file:///home/mzych/PycharmProjects/artemis-pymulation/src/telemetry.py):** Funkcja [format_telemetry](file:///home/mzych/PycharmProjects/artemis-pymulation/src/telemetry.py#L1) generuje strukturę HTML dla panelu telemetrycznego na podstawie aktualnych parametrów lotu zebranych przez symulator.
- **[src/main.py](file:///home/mzych/PycharmProjects/artemis-pymulation/src/main.py):** Główna funkcja [main](file:///home/mzych/PycharmProjects/artemis-pymulation/src/main.py#L17), która inicjalizuje obiekty, buduje interfejs użytkownika z suwakami i przyciskami, a następnie wykonuje pętlę renderowania i aktualizacji fizyki ze stałą częstotliwością odświeżania (60 klatek na sekundę).

---

## 💻 Instalacja i Uruchomienie

### Wymagania systemowe
- **Python 3.9** lub nowszy.
- Połączenie internetowe (wymagane przy pierwszym uruchomieniu przez VPython do pobrania skryptów WebGL oraz tekstury Ziemi).

### Krok 1: Klonowanie repozytorium i przejście do folderu
```bash
git clone https://github.com/twoj-login/artemis-pymulation.git
cd artemis-pymulation
```

### Krok 2: Tworzenie i aktywacja środowiska wirtualnego (zalecane)
- **Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
- **Windows (Command Prompt):**
  ```cmd
  python -m venv .venv
  .venv\Scripts\activate
  ```
- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```

### Krok 3: Instalacja zależności
Zainstaluj wymagane pakiety (`vpython` i `setuptools` do poprawnego działania biblioteki) zdefiniowane w pliku [requirements.txt](file:///home/mzych/PycharmProjects/artemis-pymulation/requirements.txt):
```bash
pip install -r requirements.txt
```

### Krok 4: Uruchomienie symulacji
Uruchom główny skrypt aplikacji:
```bash
python src/main.py
```
Po uruchomieniu skryptu automatycznie otworzy się nowa karta w Twojej domyślnej przeglądarce internetowej (najczęściej pod adresem `http://localhost:port`), prezentując interaktywne środowisko 3D wraz z panelami kontrolnymi i telemetrią.

---

## 🎮 Poradnik Użytkownika: Jak zrealizować lot powrotny (Free Return Trajectory)?

**Trajektoria swobodnego powrotu** to taka trasa lotu, w której statek kosmiczny po opuszczeniu niskiej orbity okołoziemskiej (LEO) leci w stronę Księżyca, okrąża go (wykorzystując asystę grawitacyjną do zakrzywienia toru lotu) i powraca w atmosferę Ziemi bez konieczności ponownego uruchamiania silników głównych. Był to kluczowy element bezpieczeństwa w misjach Apollo (np. Apollo 13) oraz planowanej misji Artemis II.

### Instrukcja wykonania udanego lotu:
1. **Ustawienia domyślne:**
   Po uruchomieniu lub kliknięciu **Reset** parametry są optymalnie skonfigurowane do uzyskania poprawnej trajektorii:
   - **Exit velocity (Prędkość TLI):** `+3150 m/s` (dodawana do prędkości orbity parkingowej wynoszącej ok. $7793 \text{ m/s}$, co daje prędkość startową $10\ 943 \text{ m/s}$).
   - **Mission start angle (Kąt statku):** `120 deg` (kąt na orbicie parkingowej mierzony od osi X).
   - **Moon position angle (Kąt Księżyca):** `244 deg` (początkowe przesunięcie fazowe Księżyca).
2. **Start symulacji:** Kliknij zielony przycisk **Launch Mission**.
3. **Przebieg misji:**
   - Statek zaczyna oddalać się od Ziemi w kierunku orbity Księżyca.
   - Możesz kliknąć przycisk **Faster** kilkukrotnie, aby przyspieszyć upływ czasu (domyślny krok czasu rzeczywistego można przyspieszyć do prędkości rzędu kilkunastu godzin na sekundę).
   - Po około 3-4 dniach wirtualnych statek wejdzie w sferę grawitacyjną Księżyca, okrąży go od tyłu (patrząc zgodnie z kierunkiem ruchu orbitalnego Księżyca) i zostanie skierowany z powrotem ku Ziemi.
   - Symulacja zakończy się sukcesem (`MISSION COMPLETE`), gdy statek zbliży się do powierzchni Ziemi na wysokość poniżej ok. $1900 \text{ km}$ (wejście w gęste warstwy atmosfery / korytarz powrotny).
4. **Eksperymenty:**
   Przed kliknięciem **Launch Mission** zmień parametry początkowe za pomocą suwaków:
   - **Zbyt mała prędkość TLI** (np. `+2900 m/s`): Statek nie doleci do Księżyca i zawróci w apogeum, przechodząc w wydłużoną orbitę eliptyczną wokół Ziemi.
   - **Zbyt duża prędkość TLI** (np. `+3500 m/s`): Statek przeleci bardzo szybko obok Księżyca, a jego asysta grawitacyjna będzie niewystarczająca do zakrzywienia toru lotu z powrotem na Ziemię – statek ucieknie z układu Ziemia-Księżyc w przestrzeń heliocentryczną.
   - **Zły kąt Księżyca** (np. `180 deg`): Statek minie Księżyc w dużej odległości, nie doświadczając asysty grawitacyjnej, co uniemożliwi bezpieczny powrót.

---

## 📄 Licencja

Projekt jest rozpowszechniany na warunkach licencji MIT. Pełna treść licencji znajduje się w pliku [LICENSE](file:///home/mzych/PycharmProjects/artemis-pymulation/LICENSE).

---

*Symulacja opracowana w celach dydaktycznych jako projekt demonstrujący zastosowanie metod numerycznych w fizyce i mechanice kosmicznej.*
