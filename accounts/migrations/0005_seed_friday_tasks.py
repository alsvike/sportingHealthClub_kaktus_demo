from django.db import migrations


def create_friday_tasks(apps, schema_editor):
    CleaningTask = apps.get_model('accounts', 'CleaningTask')
    friday_tasks = [
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
    ]

    for it in friday_tasks:
        title = it.get('title') or ''
        if not CleaningTask.objects.filter(weekday=4, title=title).exists():
            CleaningTask.objects.create(
                weekday=4,
                time=it.get('time',''),
                area=it.get('area',''),
                title=title,
                details=it.get('details',''),
                status='Pending',
            )


def remove_friday_tasks(apps, schema_editor):
    CleaningTask = apps.get_model('accounts', 'CleaningTask')
    titles = [
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
    ]
    CleaningTask.objects.filter(weekday=4, title__in=titles).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_seed_cleaning_tasks'),
    ]

    operations = [
        migrations.RunPython(create_friday_tasks, remove_friday_tasks),
    ]
