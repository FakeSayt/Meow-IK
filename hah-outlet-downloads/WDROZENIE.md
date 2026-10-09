# Aktualizacja HAH Outlet

Przygotowano odświeżony sklep i panel administratora na podstawie przesłanego archiwum `homeftp-1791565209.zip`. Aktualizacja działa z obecną strukturą bazy danych i PHP 8.1 lub nowszym, używanym przez istniejący sklep. Testy wykonano na PHP 8.4 i MariaDB 11.8.

## Co się zmieniło

- Spójny wygląd w kolorach kremowym i bordowym, nowa ilustracja kolekcji, czytelniejsze karty produktów i koszyk.
- Menu na telefonie i lepsze dopasowanie sklepu oraz panelu do małych ekranów.
- Ulubione zapisywane w tej przeglądarce; zmiany synchronizują się między otwartymi kartami sklepu. Lista nie jest powiązana z kontem i nie przenosi się między urządzeniami. Przy zablokowanej pamięci działa do odświeżenia strony.
- Filtry rozmiaru i dostępności, połączone z istniejącą wyszukiwarką i kategoriami; licznik wyników oraz czyszczenie filtrów.
- Panel z sekcjami: Pulpit, Produkty, Zamówienia, Zakupy LIVE, Promocje i vouchery, Ustawienia. Można otworzyć konkretną sekcję bezpośrednio z adresu strony.
- Wyszukiwanie produktów po nazwie, rozmiarze, materiale, kodzie lub ID; filtry produktów ukrytych, widocznych, wyprzedanych i z małym stanem.
- Wyszukiwanie zamówień, filtry statusów i polskie opisy statusów.
- Czytelniejsze podsumowanie istniejących statystyk oraz szybki dostęp do produktów z małym stanem.

## Wgranie na istniejący hosting

1. Zrób kopię obecnych plików sklepu. Zachowaj także standardową kopię bazy danych na hostingu.
2. Rozpakuj `HAH-Outlet-aktualizacja.zip` na komputerze.
3. Wgraj zawartość folderu `hahoutlet/` do istniejącego folderu sklepu, np. `public_html/hahoutlet/`. Podmień cztery istniejące pliki i dodaj cztery nowe pliki wymienione niżej. Wgraj komplet aktualizacji razem.
4. Pozostaw dotychczasową konfigurację `private/`, katalog `uploads/`, sesje i bazę danych. Paczka nie zawiera tych danych ani haseł. Do tej aktualizacji nie importuj ponownie przesłanego pliku SQL.
5. Odśwież stronę i panel. Gdy hosting ma dodatkowy cache, wyczyść go. Sprawdź menu mobilne, ulubione, filtr rozmiaru, koszyk, logowanie i zapis produktu.
6. Sprawdź wysyłkę e-mail oraz Facebook LIVE na docelowym hostingu. Lokalne testy korzystały z odbiornika wiadomości testowych, bez wysyłania poczty na zewnątrz. Sam Facebook decyduje o możliwości osadzenia transmisji.

Pliki zastępowane:

- `index.php`
- `admin.php`
- `app.js`
- `style.css`

Nowe pliki:

- `design.css`
- `shop-features.js`
- `admin-ui.js`
- `boutique.svg`

Nie potrzeba migracji bazy danych. Obsługa zamówień, płatności przelewem, rezerwacji LIVE, promocji, voucherów oraz przesyłania zdjęć korzysta z istniejącego zaplecza PHP.

Przy wyłączonym JavaScript panel zachowuje istniejące formularze i nawigację do sekcji na jednej stronie. Filtry i ulubione wymagają JavaScript, podobnie jak dotychczasowy koszyk sklepu.

## Weryfikacja i podglądy

Testy obejmują ulubione po odświeżeniu i w dwóch kartach, brak dostępu do pamięci przeglądarki, łączenie filtrów, zmianę dostępnych rozmiarów, menu mobilne, zachowanie fokusu klawiatury, nawigację panelu, filtrowanie magazynu i zamówień, zapis stanu, kontrast etykiet oraz szerokość widoków mobilnych.

Test integracyjny przeszedł przez koszyk, formularz zamówienia, zapis do lokalnej bazy, dwie wiadomości w lokalnym odbiorniku testowym i potwierdzenie wpłaty w panelu. Sprawdzono też odpowiedź katalogu, odrzucenie żądania bez CSRF oraz odrzucenie rezerwacji poza LIVE.

Podglądy PNG wykonano na fikcyjnych produktach i zamówieniach. Przesłane archiwum nie zawiera zdjęć produktów; nie dodawano fikcyjnych zdjęć ani produktów do paczki aktualizacji. Na hostingu sklep pokaże istniejące zdjęcia z `uploads/`.

Nie wdrożono zmian na Twoim hostingu. Paczka jest gotowa do wgrania.

## Powrót do poprzedniej wersji

Przywróć cztery podmienione pliki z kopii oraz usuń cztery nowe pliki. Ta aktualizacja nie zmienia struktury ani zawartości bazy danych.
