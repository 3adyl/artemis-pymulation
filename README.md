# Artemis II Trajectory Simulation (`artemis-pymulation`)

Trójwymiarowa, interaktywna symulacja trajektorii lotu misji kosmicznej Artemis II, zrealizowana przy użyciu biblioteki **VPython** na potrzeby projektu z fizyki.

Symulacja pozwala na badanie mechaniki nieba oraz planowanie trajektorii swobodnego powrotu (ang. *free return trajectory*) dla statku kosmicznego podróżującego z Ziemi w okolice Księżyca i z powrotem.

## 🚀 Funkcje symulacji

- **Wizualizacja 3D w czasie rzeczywistym:** Realistycznie wyskalowane modele Ziemi (z teksturą), Księżyca oraz statku kosmicznego z dynamicznie generowanym śladem lotu (trajektorią).
- **Interaktywny Panel Sterowania:**
  - **Suwak prędkości ucieczki (Exit velocity):** Regulacja prędkości początkowej manewru TLI (*Trans-Lunar Injection*) względem prędkości orbity parkingowej.
  - **Suwak kąta startu misji (Mission start angle):** Określenie położenia statku na orbicie początkowej w momencie odpalenia silników.
  - **Suwak kąta położenia Księżyca (Moon position angle):** Ustalenie fazy Księżyca w momencie rozpoczęcia manewru ucieczki.
  - **Sterowanie czasem:** Możliwość przyspieszania/zwalniania symulacji (*Faster* / *Slower*), zatrzymywania (*Pause*) oraz resetowania parametrów do domyślnych (*Reset*).
- **Panel Telemetrii (HUD):** Nowoczesny interfejs w stylu "dark mode", pokazujący na bieżąco:
  - Aktualny stan misji (`AWAITING LAUNCH`, `IN FLIGHT`, `PAUSED`, `MISSION COMPLETE`).
  - Czas misji (MET – *Mission Elapsed Time*) w dniach, godzinach, minutach i sekundach.
  - Wysokość i prędkość statku kosmicznego względem Ziemi.
  - Wysokość i prędkość statku kosmicznego względem Księżyca.

## 📐 Podstawy Fizyczne i Numeryczne

Symulacja bazuje na uproszczonym problemie trzech ciał (Ziemia, Księżyc, statek kosmiczny), gdzie masa statku kosmicznego jest zaniedbywalnie mała w porównaniu z masami Ziemi i Księżyca.

### Równania ruchu
Statek podlega grawitacji Ziemi i Księżyca zgodnie z zależnością:
$$\vec{a}_{ship} = - \frac{G M_{earth}}{|\vec{r}_{se}|^3} \vec{r}_{se} + \frac{G M_{moon}}{|\vec{r}_{sm}|^3} \vec{r}_{sm}$$

gdzie:
- $\vec{r}_{se}$ to wektor od statku do Ziemi,
- $\vec{r}_{sm}$ to wektor od Księżyca do statku.

### Metoda całkowania
- **Statek kosmiczny:** Zastosowano zaawansowany integrator **Rungego-Kutty IV rzędu (RK4)** (funkcja `rk4`), zapewniający wysoką stabilność numeryczną oraz dokładność przy dynamicznych zmianach pola grawitacyjnego podczas przelotu w pobliżu Księżyca.
- **Księżyc:** Ruch wokół Ziemi całkowany jest metodą Eulera-Cromera (funkcja `euler_moon`), z orbitą o promieniu $384\ 400 \text{ km}$ i prędkością orbitalną ok. $1022 \text{ m/s}$.

## 🛠️ Wymagania i Instalacja

Do uruchomienia projektu wymagany jest Python w wersji 3.9 lub nowszej.

1. **Instalacja bibliotek:**
   Projekt korzysta z biblioteki `vpython`, która uruchamia interaktywne okno symulacji w przeglądarce internetowej. Aby zainstalować wymagane zależności, uruchom:
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Uruchomienie

Aby rozpocząć symulację, uruchom plik główny:
```bash
python main.py
```
Po uruchomieniu skryptu otworzy się karta w domyślnej przeglądarce internetowej pod adresem lokalnym (np. `http://localhost:port`), wyświetlająca wizualizację 3D wraz z panelami kontrolnymi i telemetrią.

### Jak zrealizować udany lot powrotny (Free Return Trajectory)?
W celu uzyskania trajektorii zbliżonej do rzeczywistej misji Artemis II (czyli powrotu na Ziemię po okrążeniu Księżyca bez dodatkowego użycia napędu):
1. Pozostaw parametry domyślne (Kąt statku: $120^\circ$, Kąt Księżyca: $244^\circ$, Prędkość ucieczki: $+3150 \text{ m/s}$).
2. Kliknij **Launch Mission**.
3. Obserwuj, jak statek wykonuje asystę grawitacyjną wokół Księżyca i wraca w atmosferę Ziemi (misja zakończy się statusem `MISSION COMPLETE` po powrocie lub po upływie 13 dni wirtualnych).
4. Możesz eksperymentować z suwakami przed kliknięciem **Launch Mission**, aby sprawdzić wpływ prędkości i kątów na ostateczną trajektorię statku (np. zderzenie z Księżycem, ucieczka z układu Ziemia-Księżyc).

## 📄 Licencja

Projekt jest udostępniany na licencji MIT. Szczegóły znajdują się w pliku `LICENSE`.

***

*Symulacja przygotowana w celach edukacyjnych na zaliczenie przedmiotu fizyka.*
