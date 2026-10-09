# HAH Outlet — filtry, kolekcja i potwierdzenie wpłaty

## Wgranie aktualizacji

1. Zachowaj kopię obecnych plików i bazy.
2. Rozpakuj `HAH-Outlet-filtry-potwierdzenie-wplaty.zip`.
3. Wgraj wszystkie **13 plików** z folderu `hahoutlet/` do folderu istniejącego sklepu, zastępując starsze pliki. Nowy plik `payment_confirmation.php` też musi zostać wgrany.
4. Odśwież sklep i panel przez Ctrl+F5. Skrypty mają nowy numer wersji, aby przeglądarka pobrała aktualne pliki.
5. Baza uzupełni potrzebne kolumny automatycznie. Nie importuj ponownie SQL i nie podmieniaj konfiguracji `private/` ani zdjęć w `uploads/`.

Paczka zawiera poprzednią aktualizację etapów zamówień, wiadomości i voucherów oraz nowe poprawki. Zawiera także `shop-features.js` i `style.css`, żeby zachować zgodność skryptów filtrów i wyglądu.

## Filtry i komunikaty

Na komputerze kategorie zawijają się w panelu filtrów. Na telefonie wybierz kategorię z listy, bez przewijania długiego rzędu. Wyszukiwanie, rozmiar, dostępność, sortowanie i ulubione nadal działają razem. Przycisk wyczyszczenia resetuje filtry.

Po pobraniu kolekcji pojawia się liczba produktów, również gdy wynosi zero. Dodatkowe pobieranie rezerwacji nie blokuje wyświetlenia produktów. Przy błędzie pobrania kolekcji pojawia się informacja oraz „Spróbuj ponownie”; przy nieudanym odświeżeniu już pobrane produkty pozostają widoczne. Dostępność rezerwacji i zakupów jest sprawdzana na serwerze.

## Potwierdzenie wpłaty

Po zaksięgowaniu przelewu kliknij **Potwierdź wpłatę**. Status i stan magazynowy zostaną zapisane, a sklep wyśle klientowi wiadomość HTML z wersją tekstową, numerem zamówienia, kwotą i informacją o przygotowaniu zakupów. Wiadomość nie jest dokumentem fiskalnym.

W panelu widać wynik przekazania potwierdzenia do poczty. Odrzucenie wiadomości przez hosting nie cofa płatności. W razie błędu użyj formularza **Wyślij potwierdzenie wpłaty**; ponowienie nie odejmuje towaru ponownie. Po zaakceptowaniu wiadomości przez pocztę zwykłe powtórne kliknięcie nie wysyła duplikatu. Przy przerwaniu próby wynik może być niepewny: po pięciu minutach panel zaleca sprawdzenie poczty hostingu i nie udostępnia ponowienia, żeby nie wysłać duplikatu. Przekazanie do poczty nie jest potwierdzeniem doręczenia.

Nowe zamówienia mają zapisany e-mail. Dla starszych opłaconych zamówień można wpisać e-mail w formularzu potwierdzenia na podstawie pierwotnego zamówienia. Aktualizacja nie wysyła automatycznie wiadomości do wszystkich dawnych zamówień.

Etapy pozostają: **Opłacone → Kompletowanie → Wysłane**. Wiadomość o wysyłce jest osobna i zawiera przewoźnika, numer przesyłki i link ePaka.

## Facebook LIVE

Przycisk **Oglądaj na Facebooku** otwiera Facebooka w osobnej karcie. Po powrocie do sklepu wpisz kod produktu z transmisji. Osadzony odtwarzacz jest opcjonalny, uruchamiany przyciskiem „Spróbuj oglądać na tej stronie”. Popup z osadzonym filmem nie omija blokad Facebooka ani przeglądarki. Paczka nie gwarantuje odtwarzania konkretnej transmisji w osadzonym odtwarzaczu.

Instrukcję poprzedniej aktualizacji znajdziesz też w paczce: `ZAMOWIENIA-LIVE-MAILE-WDROZENIE.md`. Dla tej aktualizacji obowiązuje komplet **13 plików**, a nie 10 wymienionych w starszej instrukcji.

Folder `podglady/` zawiera filtry na komputerze i telefonie oraz nowy mail na fikcyjnych danych. Podglądów nie trzeba wgrywać na hosting. Paczka nie zawiera haseł, SQL, sesji ani danych klientów. Zmiany przetestowano lokalnie; rzeczywiste doręczanie wiadomości zależy od poczty na Twoim hostingu.
