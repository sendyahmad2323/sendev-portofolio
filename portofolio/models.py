"""Models for SenDev's editable Django portfolio."""
from django.db import models


class SiteProfile(models.Model):
    name = models.CharField(max_length=120, default="Sendy Ahmad")
    brand = models.CharField(max_length=50, default="SenDev")
    role = models.CharField(max_length=120, default="Full-Stack Developer")
    headline = models.CharField(max_length=200, default="Crafting digital experiences")
    tagline = models.TextField(default="Saya membangun pengalaman digital yang cepat, interaktif, dan punya karakter.")
    about = models.TextField(blank=True, default="Saya percaya website terbaik lahir dari perpaduan engineering yang rapi, desain yang berani, dan pengalaman pengguna yang dipikirkan dengan matang.")
    avatar = models.ImageField(upload_to="profile/", blank=True, null=True, help_text="Foto profil (disarankan 900×1100 px, portrait, JPG/WEBP)")
    about_photo = models.ImageField(upload_to="profile/", blank=True, null=True, help_text="Foto lain tentang kamu (disarankan 1200×900 px)")
    resume = models.FileField(upload_to="profile/cv/", blank=True, null=True, help_text="CV dalam format PDF")
    email = models.EmailField(default="sendyahmad414@gmail.com")
    location = models.CharField(max_length=120, default="Samarinda, Indonesia")
    github_url = models.URLField(blank=True, default="https://github.com/sendyahmad2323")
    linkedin_url = models.URLField(blank=True, default="https://www.linkedin.com/in/sendy-ahmad")
    instagram_url = models.URLField(blank=True, default="https://www.instagram.com/seensen_y/")
    whatsapp_url = models.URLField(blank=True, help_text="Opsional: link wa.me dengan nomor milikmu")
    available_for_work = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Profil situs"
        verbose_name_plural = "Profil situs"

    def __str__(self):
        return f"{self.brand} — {self.name}"


class Project(models.Model):
    CATEGORY_CHOICES = [
        ("web", "Web Development"),
        ("backend", "Backend / System"),
        ("mobile", "Mobile App"),
        ("ui", "UI / UX"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    tech_stack = models.CharField(max_length=300, help_text="Pisahkan dengan koma. Contoh: Django, Python, PostgreSQL")
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="web")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title


class Skill(models.Model):
    SKILL_CATEGORIES = [
        ("frontend", "Frontend"),
        ("backend", "Backend"),
        ("database", "Database"),
        ("mobile", "Mobile"),
        ("tools", "Tools"),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES)
    proficiency = models.PositiveIntegerField(default=50)
    icon = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.category})"


class Experience(models.Model):
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.position} at {self.company}"


class Certificate(models.Model):
    title = models.CharField(max_length=160)
    issuer = models.CharField(max_length=140)
    image = models.ImageField(upload_to="certificates/", help_text="Scan/foto sertifikat (disarankan 1600×1100 px)")
    issued_date = models.DateField(blank=True, null=True)
    credential_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-issued_date", "-id"]
        verbose_name = "Sertifikat"
        verbose_name_plural = "Sertifikat"

    def __str__(self):
        return self.title


class Activity(models.Model):
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, default="Kegiatan")
    image = models.ImageField(upload_to="activities/", help_text="Dokumentasi kegiatan (disarankan 1400×1100 px)")
    date = models.DateField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-date", "-id"]
        verbose_name = "Kegiatan"
        verbose_name_plural = "Kegiatan"

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=160)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Pesan masuk"
        verbose_name_plural = "Pesan masuk"

    def __str__(self):
        return f"{self.name} — {self.subject}"
