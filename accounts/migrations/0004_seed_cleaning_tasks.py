from django.db import migrations


def create_cleaning_tasks(apps, schema_editor):
    CleaningTask = apps.get_model('accounts', 'CleaningTask')

    defaults_by_weekday = {
        0: [
            {'time': '06:45', 'area': 'morning', 'title': 'Sørg for der er pænt og ryddeligt', 'details': 'Omklædningen: Gulv er pænt, skabene er lukket. Centeret: Gulvet er ryddet for udstyr som ligger og flyder'},
            {'time': '', 'area': 'morning', 'title': 'Vask/støvsug reception fra trappen og ned samt foran ansigtsscanner', 'details': ''},
            {'time': '', 'area': 'morning', 'title': 'Puds møllen', 'details': ''},
            {'time': '', 'area': 'morning', 'title': 'Vask cardio udstyr på begge etager', 'details': 'Rengøring af løbebånd, cykler, stepmaskiner, romaskiner, crosstrainer'},
            {'time': '06:45', 'area': 'morning', 'title': 'Åbn terasse døren når det er sæson', 'details': ''},
            {'time': '', 'area': 'morning', 'title': 'Sæt massage pistoler i display', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Tjek alle steder og opfyld evt. sæbe og papir. Fyld op af vatpinde, deo mm i kassen ude hos damerne', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Tøm alle skraldespande i omklædningen. Dette kan undlades i træningsområdet hvis der ikke er andet end papir i og de er halvt fyldte', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Husk at lås døren til terrassen', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Tag massage pistoler af display og sæt dem til opladning ude i p-rummet', 'details': ''},
        ],
        1: [
            {'time': '06:45', 'area': 'morning', 'title': 'Sørg der er pænt og ryddeligt', 'details': 'Omklædningen: Gulv er pænt, skabene er lukket. Centeret: Gulvet er ryddet for udstyr som ligger og flyder'},
            {'time': '', 'area': 'morning', 'title': 'Vask/støvsug reception fra trappen og ned samt foran ansigtsscanner', 'details': ''},
            {'time': '', 'area': 'morning', 'title': 'Puds møllen', 'details': ''},
            {'time': '', 'area': 'morning', 'title': 'Vask udstyr på 1 sal. Maskiner og rack', 'details': 'Udstyr med vægte såsom styrkemaskiner, racks/stativer samt træningsbænke'},
            {'time': '06:45', 'area': 'morning', 'title': 'Åbn terasse døren når det er sæson', 'details': ''},
            {'time': '', 'area': 'morning', 'title': 'Sæt massage pistoler i display', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Tjek alle steder og opfyld evt. sæbe og papir. Fyld op af vatpinde, deo mm i kassen ude hos damerne', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Tøm alle skraldespande i omklædningen. Dette kan undlades i træningsområdet hvis der ikke er andet end papir i og de er halvt fyldte', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Husk at lås døren til terrassen', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Tag massage pistoler af display og sæt dem til opladning ude i p-rummet', 'details': ''},
        ],
        2: [
            {'time': '06:45', 'area': 'morning', 'title': 'Sørg der er pænt og ryddeligt', 'details': 'Omklædningen: Gulv er pænt, skabene er lukket. Centeret: Gulvet er ryddet for udstyr som ligger og flyder'},
            {'time': '', 'area': 'morning', 'title': 'Vask/støvsug reception fra trappen og ned samt foran ansigtsscanner', 'details': ''},
            {'time': '', 'area': 'morning', 'title': 'Puds møllen', 'details': ''},
            {'time': '', 'area': 'morning', 'title': 'Vask cardio udstyr på begge etager', 'details': 'Rengøring af løbebånd, cykler, stepmaskiner, romaskiner,crosstrainer'},
            {'time': '06:45', 'area': 'morning', 'title': 'Åbn terasse døren når det er sæson', 'details': ''},
            {'time': '', 'area': 'morning', 'title': 'Sæt massage pistoler i display', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Tjek alle steder og opfyld evt. sæbe og papir. Fyld op af vatpinde, deo mm i kassen ude hos damerne', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Tøm alle skraldespande i omklædningen. Dette kan undlades i træningsområdet hvis der ikke er andet end papir i og de er halvt fyldte', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Husk at lås døren til terrassen', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Tag massage pistoler af display og sæt dem til opladning ude i p-rummet', 'details': ''},
        ],
        3: [
            {'time': '06:45', 'area': 'morning', 'title': 'Sørg der er pænt og ryddeligt', 'details': 'Omklædningen: Gulv er pænt, skabene er lukket. Centeret: Gulvet er ryddet for udstyr som ligger og flyder'},
            {'time': '', 'area': 'morning', 'title': 'Vask/støvsug reception fra trappen og ned samt foran ansigtsscanner', 'details': ''},
            {'time': '', 'area': 'morning', 'title': 'Puds møllen', 'details': ''},
            {'time': '', 'area': 'morning', 'title': 'Vask udstyr på 1 sal. Maskiner og rack', 'details': 'Udstyr med vægte såsom styrkemaskiner, racks/stativer samt træningsbænke'},
            {'time': '06:45', 'area': 'morning', 'title': 'Åbn terasse døren når det er sæson', 'details': ''},
            {'time': '', 'area': 'morning', 'title': 'Sæt massage pistoler i display', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Tjek alle steder og opfyld evt. sæbe og papir. Fyld op af vatpinde, deo mm i kassen ude hos damerne', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Tøm alle skraldespande i omklædningen. Dette kan undlades i træningsområdet hvis der ikke er andet end papir i og de er halvt fyldte', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Husk at lås døren til terrassen', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Tag massage pistoler af display og sæt dem til opladning ude i p-rummet', 'details': ''},
        ],
        4: [
            {'time': '06:45', 'area': 'morning', 'title': 'Sørg der er pænt og ryddeligt', 'details': ''},
            {'time': '', 'area': 'morning', 'title': 'Vask/støvsug reception fra trappen og ned samt foran ansigtsscanner', 'details': ''},
            {'time': '', 'area': 'morning', 'title': 'Puds møllen', 'details': ''},
            {'time': '', 'area': 'morning', 'title': 'Vask cardio udstyr på begge etager', 'details': ''},
            {'time': '06:45', 'area': 'morning', 'title': 'Åbn terasse døren når det er sæson', 'details': ''},
            {'time': '', 'area': 'morning', 'title': 'Sæt massage pistoler i display', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Tjek alle steder og opfyld evt. sæbe og papir. Fyld op af vatpinde, deo mm i kassen ude hos damerne', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Tøm alle skraldespande i omklædningen. Dette kan undlades i træningsområdet hvis der ikke er andet end papir i og de er halvt fyldte', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Husk at lås døren til terrassen', 'details': ''},
            {'time': '15:00', 'area': 'evening', 'title': 'Tag massage pistoler af display og sæt dem til opladning ude i p-rummet', 'details': ''},
        ],
    }

    for wk, items in defaults_by_weekday.items():
        for it in items:
            title = it.get('title') or ''
            if not CleaningTask.objects.filter(weekday=wk, title=title).exists():
                CleaningTask.objects.create(
                    weekday=wk,
                    time=it.get('time',''),
                    area=it.get('area',''),
                    title=title,
                    details=it.get('details',''),
                    status='Pending',
                )


def remove_cleaning_tasks(apps, schema_editor):
    CleaningTask = apps.get_model('accounts', 'CleaningTask')
    titles_to_remove = []
    defaults_by_weekday = {
        0: [
            'Sørg for der er pænt og ryddeligt',
            'Vask/støvsug reception fra trappen og ned samt foran ansigtsscanner',
            'Puds møllen',
            'Vask cardio udstyr på begge etager',
            'Åbn terasse døren når det er sæson',
            'Sæt massage pistoler i display',
            'Tjek alle steder og opfyld evt. sæbe og papir. Fyld op af vatpinde, deo mm i kassen ude hos damerne',
            'Tøm alle skraldespande i omklædningen. Dette kan undlades i træningsområdet hvis der ikke er andet end papir i og de er halvt fyldte',
            'Husk at lås døren til terrassen',
            'Tag massage pistoler af display og sæt dem til opladning ude i p-rummet',
        ],
        1: [
            'Sørg der er pænt og ryddeligt',
            'Vask/støvsug reception fra trappen og ned samt foran ansigtsscanner',
            'Puds møllen',
            'Vask udstyr på 1 sal. Maskiner og rack',
            'Åbn terasse døren når det er sæson',
            'Sæt massage pistoler i display',
            'Tjek alle steder og opfyld evt. sæbe og papir. Fyld op af vatpinde, deo mm i kassen ude hos damerne',
            'Tøm alle skraldespande i omklædningen. Dette kan undlades i træningsområdet hvis der ikke er andet end papir i og de er halvt fyldte',
            'Husk at lås døren til terrassen',
            'Tag massage pistoler af display og sæt dem til opladning ude i p-rummet',
        ],
        2: [
            'Sørg der er pænt og ryddeligt',
            'Vask/støvsug reception fra trappen og ned samt foran ansigtsscanner',
            'Puds møllen',
            'Vask cardio udstyr på begge etager',
            'Åbn terasse døren når det er sæson',
            'Sæt massage pistoler i display',
            'Tjek alle steder og opfyld evt. sæbe og papir. Fyld op af vatpinde, deo mm i kassen ude hos damerne',
            'Tøm alle skraldespande i omklædningen. Dette kan undlades i træningsområdet hvis der ikke er andet end papir i og de er halvt fyldte',
            'Husk at lås døren til terrassen',
            'Tag massage pistoler af display og sæt dem til opladning ude i p-rummet',
        ],
        3: [
            'Sørg der er pænt og ryddeligt',
            'Vask/støvsug reception fra trappen og ned samt foran ansigtsscanner',
            'Puds møllen',
            'Vask udstyr på 1 sal. Maskiner og rack',
            'Åbn terasse døren når det er sæson',
            'Sæt massage pistoler i display',
            'Tjek alle steder og opfyld evt. sæbe og papir. Fyld op af vatpinde, deo mm i kassen ude hos damerne',
            'Tøm alle skraldespande i omklædningen. Dette kan undlades i træningsområdet hvis der ikke er andet end papir i og de er halvt fyldte',
            'Husk at lås døren til terrassen',
            'Tag massage pistoler af display og sæt dem til opladning ude i p-rummet',
        ],
        4: [
            'Sørg der er pænt og ryddeligt',
            'Vask/støvsug reception fra trappen og ned samt foran ansigtsscanner',
            'Puds møllen',
            'Vask cardio udstyr på begge etager',
            'Åbn terasse døren når det er sæson',
            'Sæt massage pistoler i display',
            'Tjek alle steder og opfyld evt. sæbe og papir. Fyld op af vatpinde, deo mm i kassen ude hos damerne',
            'Tøm alle skraldespande i omklædningen. Dette kan undlades i træningsområdet hvis der ikke er andet end papir i og de er halvt fyldte',
            'Husk at lås døren til terrassen',
            'Tag massage pistoler af display og sæt dem til opladning ude i p-rummet',
        ],
    }

    for wk, titles in defaults_by_weekday.items():
        CleaningTask.objects.filter(weekday=wk, title__in=titles).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_cleaningtask_alter_trial_status_and_more'),
    ]

    operations = [
        migrations.RunPython(create_cleaning_tasks, remove_cleaning_tasks),
    ]
