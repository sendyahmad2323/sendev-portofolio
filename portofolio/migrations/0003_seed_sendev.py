"""Copy the 4 projects from the original upload into the admin-editable database.

Never delete user data in reverse migration.
"""
from django.db import migrations


def seed_initial_content(apps, schema_editor):
    Project = apps.get_model('portofolio', 'Project')
    SiteProfile = apps.get_model('portofolio', 'SiteProfile')
    if not SiteProfile.objects.exists():
        SiteProfile.objects.create(
            name='Sendy Ahmad', brand='SenDev', role='Full-Stack Developer',
            tagline='Saya membangun pengalaman digital yang cepat, interaktif, dan punya karakter.',
            about='Saya adalah developer yang tertarik mengubah ide kompleks menjadi produk digital yang sederhana digunakan, rapi di balik layar, dan berkesan sejak detik pertama.',
            email='sendyahmad414@gmail.com', location='Samarinda, Indonesia',
            github_url='https://github.com/sendyahmad2323',
            linkedin_url='https://www.linkedin.com/in/sendy-ahmad',
            instagram_url='https://www.instagram.com/seensen_y/',
        )
    if Project.objects.exists():
        return
    projects = [
        ('Framework Decision Support System', 'Sistem pendukung keputusan pemilihan framework terbaik dengan metode Simple Additive Weighting (SAW).', 'Python, Django, SAW', 'https://github.com/sendyahmad2323/saw_spk', 'backend'),
        ('Blogging Platform with Django', 'Platform blogging dengan struktur backend Django dan pengalaman membaca yang lebih terorganisasi.', 'Django, Python, HTML/CSS', 'https://github.com/sendyahmad2323/Blogging-Django', 'web'),
        ('PPID BAZNAS Kalimantan Timur', 'Website layanan informasi publik untuk mendukung akses informasi dan layanan digital.', 'Web, Public Service, UI', 'https://github.com/Sheyon565/ppid-baznas-kaltim', 'web'),
        ('Islamic Android Application', 'Aplikasi Android bertema Islami yang dikembangkan menggunakan Kotlin dan Android Studio.', 'Kotlin, Android Studio, Mobile', 'https://github.com/sendyahmad2323/islamic', 'mobile'),
    ]
    for i, (title, description, tech_stack, github_url, category) in enumerate(projects, 1):
        Project.objects.create(title=title, description=description, tech_stack=tech_stack,
                               github_url=github_url, category=category, featured=True, order=i)


class Migration(migrations.Migration):
    dependencies = [('portofolio', '0002_sendev_content')]
    operations = [migrations.RunPython(seed_initial_content, migrations.RunPython.noop)]
