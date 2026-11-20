from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('portofolio', '0001_initial')]

    operations = [
        migrations.AddField(model_name='project', name='category', field=models.CharField(choices=[('web', 'Web Development'), ('backend', 'Backend / System'), ('mobile', 'Mobile App'), ('ui', 'UI / UX')], default='web', max_length=20)),
        migrations.AddField(model_name='project', name='order', field=models.PositiveIntegerField(default=0)),
        migrations.AlterModelOptions(name='project', options={'ordering': ['order', '-created_at']}),
        migrations.AlterField(model_name='skill', name='category', field=models.CharField(choices=[('frontend', 'Frontend'), ('backend', 'Backend'), ('database', 'Database'), ('mobile', 'Mobile'), ('tools', 'Tools')], max_length=20)),
        migrations.CreateModel(
            name='SiteProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Sendy Ahmad', max_length=120)),
                ('brand', models.CharField(default='SenDev', max_length=50)),
                ('role', models.CharField(default='Full-Stack Developer', max_length=120)),
                ('headline', models.CharField(default='Crafting digital experiences', max_length=200)),
                ('tagline', models.TextField(default='Saya membangun pengalaman digital yang cepat, interaktif, dan punya karakter.')),
                ('about', models.TextField(blank=True, default='Saya percaya website terbaik lahir dari perpaduan engineering yang rapi, desain yang berani, dan pengalaman pengguna yang dipikirkan dengan matang.')),
                ('avatar', models.ImageField(blank=True, help_text='Foto profil (disarankan 900×1100 px, portrait, JPG/WEBP)', null=True, upload_to='profile/')),
                ('about_photo', models.ImageField(blank=True, help_text='Foto lain tentang kamu (disarankan 1200×900 px)', null=True, upload_to='profile/')),
                ('resume', models.FileField(blank=True, help_text='CV dalam format PDF', null=True, upload_to='profile/cv/')),
                ('email', models.EmailField(default='sendyahmad414@gmail.com', max_length=254)),
                ('location', models.CharField(default='Samarinda, Indonesia', max_length=120)),
                ('github_url', models.URLField(blank=True, default='https://github.com/sendyahmad2323')),
                ('linkedin_url', models.URLField(blank=True, default='https://www.linkedin.com/in/sendy-ahmad')),
                ('instagram_url', models.URLField(blank=True, default='https://www.instagram.com/seensen_y/')),
                ('whatsapp_url', models.URLField(blank=True, help_text='Opsional: link wa.me dengan nomor milikmu')),
                ('available_for_work', models.BooleanField(default=True)),
            ],
            options={'verbose_name': 'Profil situs', 'verbose_name_plural': 'Profil situs'},
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=160)),
                ('issuer', models.CharField(max_length=140)),
                ('image', models.ImageField(help_text='Scan/foto sertifikat (disarankan 1600×1100 px)', upload_to='certificates/')),
                ('issued_date', models.DateField(blank=True, null=True)),
                ('credential_url', models.URLField(blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={'ordering': ['order', '-issued_date', '-id'], 'verbose_name': 'Sertifikat', 'verbose_name_plural': 'Sertifikat'},
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=160)),
                ('description', models.TextField(blank=True)),
                ('category', models.CharField(default='Kegiatan', max_length=100)),
                ('image', models.ImageField(help_text='Dokumentasi kegiatan (disarankan 1400×1100 px)', upload_to='activities/')),
                ('date', models.DateField(blank=True, null=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={'ordering': ['order', '-date', '-id'], 'verbose_name': 'Kegiatan', 'verbose_name_plural': 'Kegiatan'},
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=160)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
            ],
            options={'ordering': ['-created_at'], 'verbose_name': 'Pesan masuk', 'verbose_name_plural': 'Pesan masuk'},
        ),
    ]
