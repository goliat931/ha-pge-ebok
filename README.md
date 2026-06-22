# PGE eBOK - Integracja dla Home Assistant

Integracja (Custom Component) dla Home Assistant pobierająca informacje o saldzie z konta PGE eBOK (Polska Grupa Energetyczna).

Tworzy ona sensor (np. `sensor.pge_ebok_TWOJ_LOGIN`), który automatycznie loguje się do portalu eBOK i aktualizuje stan salda (w PLN) co 6 godzin.

## Instalacja przez HACS (Zalecane)

Najprostszą metodą instalacji jest wykorzystanie HACS (Home Assistant Community Store) jako niestandardowego repozytorium.

1. Otwórz **HACS** w swoim panelu Home Assistant.
2. Przejdź do zakładki **Integracje** (Integrations).
3. Kliknij na ikonę trzech kropek w prawym górnym rogu i wybierz **Niestandardowe repozytoria** (Custom repositories).
4. W polu "Repository" wklej URL tego repozytorium.
5. W polu "Category" wybierz **Integracja** (Integration) i kliknij Dodaj (Add).
6. Zamknij okno niestandardowych repozytoriów, a w wyszukiwarce HACS znajdź nowo dodaną integrację **PGE eBOK**.
7. Kliknij **Zainstaluj** (Install).
8. Po poprawnej instalacji wymagany jest **restart Home Assistant**.

## Konfiguracja (Interfejs graficzny)

Konfiguracja odbywa się przez interfejs graficzny Home Assistanta:

1. Przejdź do **Ustawienia** -> **Urządzenia i usługi**.
2. Kliknij **Dodaj integrację** w prawym dolnym rogu.
3. Wyszukaj **PGE eBOK**.
4. Wprowadź dane logowania do portalu PGE eBOK (ebok.gkpge.pl) i zatwierdź.

## Uwagi
Integracja używa techniki "web scraping", co oznacza, że w przypadku zmian na stronie internetowej PGE eBOK (np. zmiany formularza logowania, struktury widoku), integracja może przestać działać i wymagać aktualizacji kodu.

## Rozwiązywanie problemów (Troubleshooting)

### Brak integracji w wyszukiwarce HACS pomimo poprawnego dodania repozytorium
Jeśli repozytorium zostało dodane do HACS przed pojawieniem się pierwszego wydania (Release), HACS mógł zapisać w pamięci podręcznej (cache) pustą odpowiedź. Aby to rozwiązać:
1. Usuń `PGE eBOK` z sekcji *Niestandardowe repozytoria* (Custom repositories) w HACS.
2. Wyczyść pamięć podręczną przeglądarki (frontend cache).
3. Dodaj ponownie repozytorium `goliat931/ha-pge-ebok` jako *Integrację*, co wymusi pobranie najnowszych danych.
