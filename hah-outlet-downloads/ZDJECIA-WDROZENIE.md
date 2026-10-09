# HAH Outlet — poprawka dodawania i edycji zdjęć

## Wgranie poprawki

1. Zrób kopię czterech obecnych plików: `admin.php`, `admin-media.js`, `admin-media-upload.php`, `design.css`.
2. Rozpakuj `HAH-Outlet-zdjecia-v2.zip`.
3. Wgraj cztery pliki z folderu `hahoutlet/` do istniejącego folderu sklepu, np. `public_html/hahoutlet/`, zastępując stare wersje. Wgraj komplet razem.
4. Odśwież panel (Ctrl+F5). Nowy panel pobiera skrypty i style z oznaczeniem `v=30`. Wgraj zarówno skrypt JS, jak i endpoint PHP; nie wystarczy sama podmiana panelu.
5. Otwórz produkt, wybierz zdjęcia i kliknij „Zapisz produkt”.

Poprawka jest przeznaczona do wcześniej przygotowanej modernizacji HAH Outlet. Nie wymaga importu SQL ani zmian w bazie, konfiguracji private/ i istniejących zdjęciach.

## Nowy sposób dodawania zdjęć

Domyślnie wybrany jest **Zgodny z hostingiem (zalecany)**. Wysyła zdjęcie w małych porcjach przez zwykłe pola formularza. Omija przesyłanie surowych danych, które wywoływało komunikat „Niepełna część pliku”, oraz standardowy katalog tymczasowy PHP dla uploadów.

Wersja 2 zmniejsza porcję do 4 KB danych pliku. Zamiast dużego pola Base64 przesyła do 8 KB znaków szesnastkowych. To ogranicza ryzyko odrzucenia pól przez limity hostingu i filtry danych. Serwer sprawdza deklarowaną długość każdej porcji przed zapisem, a przeglądarka potwierdza liczbę przyjętych bajtów. Format oraz jakość zdjęcia pozostają bez zmian.

Podgląd automatycznie przechodzi na dane obrazu odczytane z pliku, jeśli przeglądarka lub polityka strony blokuje adres `blob:`. Nie usuwa to polityki bezpieczeństwa strony. Jeśli hosting blokuje również `data:`, podgląd lokalny nadal może być niedostępny; nie przeszkadza to w przesyłaniu pliku.

Opcja **Zwykłe przesyłanie plików** wysyła plik standardowo, pojedynczo. Jeżeli hosting odrzuci ten sposób, panel automatycznie przechodzi na tryb zgodny z hostingiem. Błąd sesji wymaga ponownego zalogowania.

W przypadku przerwanego przesyłania lub błędu walidacji produktu formularz i wybrane zdjęcia pozostają w panelu. Popraw dane, jeśli są błędne, i ponownie kliknij „Zapisz produkt”. Już przesłane zdjęcia są pamiętane do kolejnej próby w tej sesji. Jeśli zapis się udał, ale odpowiedź została utracona, identyczne ponowienie rozpozna zakończony zapis bez dodawania drugiego produktu ani zdjęcia.

Formaty zdjęć: JPG, PNG, WebP, AVIF. Maksymalnie 100 zdjęć produktu; nowe pliki wraz z filmem mogą mieć łącznie do 80 MB. Przy dużym filmie tryb zgodny z hostingiem może działać wolniej.

## Późniejsza edycja

W zakładce **Produkty** znajdź produkt i kliknij **Edytuj**. Zobaczysz zapisane zdjęcia.

- Dodawaj kolejne przez pole wyboru zdjęć.
- **Ustaw jako główne** przesuwa zdjęcie na pierwsze miejsce. To zdjęcie pokaże się na karcie produktu w sklepie.
- **Przesuń wcześniej / później** zmienia kolejność galerii.
- **Zastąp zdjęcie** pozwala wybrać nowy plik w miejscu starego.
- **Usuń zdjęcie** odłącza je od produktu.

Na końcu kliknij **Zapisz produkt**. Zmiany w galerii stają się widoczne w sklepie po zapisaniu. Przyciski nie kadrują ani nie zmieniają kolorów zdjęcia.

Usunięcie lub zastąpienie nie kasuje fizycznego pliku z katalogu uploads — chroni to zdjęcia, które mogą być używane gdzie indziej. Nie usuwaj całego katalogu uploads.

## Sprawdzenie poprawki

39 testów przeszło lokalnie, w tym przesyłanie rzeczywistych obrazów, większe zdjęcie w kilku porcjach, ponawianie, podgląd, wymiana zdjęcia, usuwanie, kolejność i zdjęcie główne. Sprawdzono też zachowanie formularza po błędzie walidacji, ponowienie zapisu po utracie odpowiedzi bez duplikatów oraz dotychczasowy koszyk, zamówienia, panel i filtry. Osobno sprawdzono przesyłanie przy file_uploads=Off, niedostępnym upload_tmp_dir i limicie post_max_size=128K.

Serwer nadal sprawdza sesję administratora, CSRF, rozmiar pliku, typ MIME i poprawność obrazu. Do produktu można przypisać tylko jego dotychczasowe zdjęcia lub pliki przesłane w bieżącej sesji administratora.

Nie potwierdzono dokładnej przyczyny niepełnego odczytu danych na Twoim hostingu, ponieważ jego logi nie są dostępne w tej sesji. W dostarczonym archiwum `.user.ini` zawiera przykładową ścieżkę `upload_tmp_dir`. Domyślny nowy tryb nie zależy od tego ustawienia. Muszą pozostać zapisywalne katalogi `private/upload-parts` i `uploads`.

Objawy ze zrzutu odtworzono lokalnie przy usuwaniu przez hosting pól formularza dłuższych niż 8192 znaki oraz polityce `img-src 'self' data:`. Publicznego adresu autobothub.pl nie udało się odczytać z tego środowiska, więc nie stwierdzono, że dokładnie te ograniczenia są ustawione na docelowym serwerze.

Jeżeli problem pozostanie, przekaż pełny komunikat błędu. H01 oznacza brak pola z danymi w żądaniu, H02 nieprawidłowe kodowanie lub rozmiar, H03 niezgodność deklarowanej i otrzymanej długości. Nie trzeba podawać hasła administratora.

Zmiany przygotowano i przetestowano lokalnie. Paczkę trzeba wgrać na hosting.
