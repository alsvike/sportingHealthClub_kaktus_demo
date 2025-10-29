# Sporting Health Club — demo

Dette repository er en lille Django‑app (app: `accounts`) lavet som demo for et personalestyringsværktøj.

Kort oversigt
- Auth (login/logout) og et staff dashboard
- Overlevering: dagligt skema med prøvetimer, rengørings‑tider, vagtbeskeder og leder‑svar (med manager‑rettigheder)
- Rengøring: personaleets ugeplan (Mandag–Søndag) med to‑shift layout og kanoniske opgaver seed'et via Django migrations
- Rollegrupper: Receptionist, Manager, Owner, Admin (kan oprettes via management command)

Vigtigt — seedede rengøringsopgaver
- De kanoniske rengøringsopgaver oprettes server‑side gennem data‑migrationer i `accounts/migrations/` (0004–0007). Det betyder at opgaverne er persistente i databasen og ikke længere oprettes fra klienten.

Hurtig start (Windows PowerShell)

1) Opret og aktiver et virtualenv

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Kør migrationer og opret superuser

```powershell
python manage.py migrate
python manage.py createsuperuser
```

3) (Valgfrit) Opret rollegrupper

```powershell
python manage.py create_roles
```

4) Start udviklingsserveren

```powershell
python manage.py runserver
```

Åbn http://127.0.0.1:8000/ — projektet vil som default kræve login for staff‑sider.

Vigtige sider
- /accounts/overlevering/ (Overlevering): kalender med daglige prøvetimer, vagt‑ og lederbeskeder samt rengørings‑tidsfelter
- /accounts/cleaning/ (Rengøring): ugefaner (Mandag–Søndag) med opgavetracking og status (Afventer/Udført/Ikke i brug/Ikke udført)

API (internt brug af frontend)
- GET /accounts/api/cleaning_tasks/?weekday=N — hent rengøringsopgaver for en ugedag (0=Mandag..6=Søndag)
- POST /accounts/api/cleaning_tasks/ — opret opgave
- PATCH /accounts/api/cleaning_tasks/<id>/ — opdater (bruges af autosave for status)
- POST /accounts/api/cleaning/ — gem rengøringsankomst/afgang for en dato
- POST /accounts/api/shift_message/ — gem vagtbesked
- POST /accounts/api/manager_message/ — gem lederbesked/reply

Design‑/UX noter
- Rengøring‑siden åbner automatisk fanen for dagens ugedag ved indlæsning.
- Autosave: frontend debouncer ændringer (600ms) og viser en "Ændringer gemt"‑notifikation når brugeren er inaktiv efter et kort interval.
- Client‑side seeding er fjernet — alle kanoniske opgaver skabes via migrations for at undgå dublering og overskrivning af brugerdata.

Udviklingstips
- For at gen‑seed (kun i udvikling) kan du rulle migrations tilbage og køre dem igen, fx:

```powershell
python manage.py migrate accounts 0003
python manage.py migrate accounts
```

- For at ændre eller tilføje flere skabelonopgaver, rediger migrationerne (`accounts/migrations/0004_*` osv.) eller tilføj en ny data migration.

Fejlfinding
- Hvis ændringer i templates ikke slår igennem, genstart dev‑serveren.
- Hvis du ikke ser seedede opgaver, tjek `python manage.py showmigrations accounts` og kør `python manage.py migrate accounts`.

Vil du have mere?
- Jeg kan: fjerne den skjulte sample‑knap fra templaten, tilføje en lille `README`‑sektion i admin eller lave en management command `seed_cleaning_tasks` for gen‑seed uden at køre migrations.

---
Opdateret: automatisk genereret README med status for rengørings‑seed og Overlevering/cleaning features.
