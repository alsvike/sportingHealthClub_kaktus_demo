from django.db import migrations


def create_saturday_tasks(apps, schema_editor):
    CleaningTask = apps.get_model('accounts', 'CleaningTask')
    saturday_tasks = [
        {'time': '', 'area': 'morning', 'title': 'Sørg der er pænt og ryddeligt', 'details': ''},
        {'time': '', 'area': 'morning', 'title': 'Vask/støvsug reception fra trappen og ned samt foran ansigtsscanner', 'details': ''},
        {'time': '', 'area': 'morning', 'title': 'Puds møllen', 'details': ''},
        {'time': '', 'area': 'morning', 'title': 'Vask udstyr på 1 sal. Maskiner og rack', 'details': ''},
        {'time': '09:00', 'area': 'morning', 'title': 'Åbn terasse døren når det er sæson', 'details': ''},
        {'time': '', 'area': 'morning', 'title': 'Sæt massage pistoler i display', 'details': ''},
        {'time': '', 'area': 'morning', 'title': 'Tjek alle steder og opfyld evt. sæbe og papir. Fyld op af vatpinde, deo mm i kassen ude hos damerne', 'details': ''},
        {'time': '', 'area': 'morning', 'title': 'Tøm alle skraldespande i omklædningen. Dette kan undlades i træningsområdet hvis der ikke er andet end papir i og de er halvt fyldte', 'details': ''},
        {'time': '', 'area': 'morning', 'title': 'Husk at lås døren til terrassen', 'details': ''},
        {'time': '', 'area': 'morning', 'title': 'Tag massage pistoler af display og sæt dem til opladning ude i p-rummet', 'details': ''},
    ]

    for it in saturday_tasks:
        title = it.get('title') or ''
        if not CleaningTask.objects.filter(weekday=5, title=title).exists():
            CleaningTask.objects.create(
                weekday=5,
                time=it.get('time',''),
                area=it.get('area',''),
                title=title,
                details=it.get('details',''),
                status='Pending',
            )


def remove_saturday_tasks(apps, schema_editor):
    CleaningTask = apps.get_model('accounts', 'CleaningTask')
    titles = [
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
    ]
    CleaningTask.objects.filter(weekday=5, title__in=titles).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_seed_friday_tasks'),
    ]

    operations = [
        migrations.RunPython(create_saturday_tasks, remove_saturday_tasks),
    ]
