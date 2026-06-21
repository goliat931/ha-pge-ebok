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

## Konfiguracja (configuration.yaml)

Obecnie integracja konfigurowana jest bezpośrednio w pliku `configuration.yaml`. Należy podać dane logowania, którymi logujesz się do portalu PGE eBOK (ebok.gkpge.pl).

Dodaj poniższy fragment do pliku `configuration.yaml`:

```yaml
sensor:
  - platform: pge_ebok
    username: "TWOJ_ADRES_EMAIL"
    password: "TWOJE_HASLO"
```

Po dodaniu wpisu, zapisz plik i **zrestartuj Home Assistant**.

### Zmienne konfiguracyjne:
- `platform`: (wymagane) musi być ustawione na `pge_ebok`
- `username`: (wymagane) Twój adres e-mail, będący loginem do profilu PGE eBOK.
- `password`: (wymagane) Twoje hasło do profilu PGE eBOK.

## Uwagi
Integracja używa techniki "web scraping", co oznacza, że w przypadku zmian na stronie internetowej PGE eBOK (np. zmiany formularza logowania, struktury widoku), integracja może przestać działać i wymagać aktualizacji kodu.
