"""One-page website + editable CMS + persistent contact messages."""
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from .models import Activity, Certificate, ContactMessage, Experience, Project, SiteProfile, Skill


FALLBACK_PROJECTS = [
    {
        "title": "Framework Decision Support System",
        "description": "Sistem pendukung keputusan pemilihan framework terbaik dengan metode Simple Additive Weighting (SAW).",
        "category": "backend", "category_label": "DECISION SUPPORT", "tech": ["Python", "Django", "SAW"],
        "github": "https://github.com/sendyahmad2323/saw_spk", "live": "", "image": "", "variant": "decision", "number": "01",
    },
    {
        "title": "Blogging Platform with Django",
        "description": "Platform blogging dengan struktur backend Django dan pengalaman membaca yang lebih terorganisasi.",
        "category": "web", "category_label": "WEB APPLICATION", "tech": ["Django", "Python", "HTML/CSS"],
        "github": "https://github.com/sendyahmad2323/Blogging-Django", "live": "", "image": "", "variant": "blog", "number": "02",
    },
    {
        "title": "PPID BAZNAS Kalimantan Timur",
        "description": "Website layanan informasi publik untuk mendukung akses informasi dan layanan digital.",
        "category": "web", "category_label": "PUBLIC SERVICE", "tech": ["Web", "Public Service", "UI"],
        "github": "https://github.com/Sheyon565/ppid-baznas-kaltim", "live": "", "image": "", "variant": "ppid", "number": "03",
    },
    {
        "title": "Islamic Android Application",
        "description": "Aplikasi Android bertema Islami yang dikembangkan menggunakan Kotlin dan Android Studio.",
        "category": "mobile", "category_label": "ANDROID APPLICATION", "tech": ["Kotlin", "Android Studio", "Mobile"],
        "github": "https://github.com/sendyahmad2323/islamic", "live": "", "image": "", "variant": "mobile", "number": "04",
    },
]

FALLBACK_SKILLS = [
    {"name": "Frontend", "number": "01", "caption": "Interfaces people love", "items": ["HTML & CSS", "JavaScript", "React", "Responsive UI"]},
    {"name": "Backend", "number": "02", "caption": "Logic built to scale", "items": ["Python", "Django", "Laravel", "REST API"]},
    {"name": "Mobile", "number": "03", "caption": "Ideas beyond the browser", "items": ["Kotlin", "Android Studio"]},
    {"name": "Workflow", "number": "04", "caption": "From concept to shipping", "items": ["Git", "GitHub", "Problem Solving"]},
]


def profile_data():
    item = SiteProfile.objects.first()
    p = {
        "name": "Sendy Ahmad", "brand": "SenDev", "role": "Full-Stack Developer",
        "headline": "Crafting digital experiences", "tagline": "Saya membangun pengalaman digital yang cepat, interaktif, dan punya karakter.",
        "about": "Saya adalah developer yang tertarik mengubah ide kompleks menjadi produk digital yang sederhana digunakan, rapi di balik layar, dan berkesan sejak detik pertama.",
        "avatar": "", "about_photo": "", "resume": "", "email": "sendyahmad414@gmail.com",
        "location": "Samarinda, Indonesia", "github_url": "https://github.com/sendyahmad2323",
        "linkedin_url": "https://www.linkedin.com/in/sendy-ahmad",
        "instagram_url": "https://www.instagram.com/seensen_y/", "whatsapp_url": "",
        "available_for_work": True,
    }
    if item:
        for field in ("name", "brand", "role", "headline", "tagline", "about", "email", "location", "github_url", "linkedin_url", "instagram_url", "whatsapp_url", "available_for_work"):
            p[field] = getattr(item, field)
        for field in ("avatar", "about_photo", "resume"):
            uploaded = getattr(item, field)
            p[field] = uploaded.url if uploaded else ""
    return p


def project_data():
    records = list(Project.objects.all())
    if not records:
        return FALLBACK_PROJECTS
    data = []
    for index, item in enumerate(records, 1):
        data.append({
            "title": item.title, "description": item.description,
            "category": item.category, "category_label": item.get_category_display().upper(),
            "tech": [x.strip() for x in item.tech_stack.split(",") if x.strip()][:5],
            "github": item.github_url or "", "live": item.live_url or "",
            "image": item.image.url if item.image else "",
            "variant": ["decision", "blog", "ppid", "mobile"][(index - 1) % 4],
            "number": f"{index:02d}",
        })
    return data


def skill_data():
    records = list(Skill.objects.all().order_by("category", "name"))
    if not records:
        return FALLBACK_SKILLS
    groups = {}
    for record in records:
        groups.setdefault(record.get_category_display(), []).append(record.name)
    return [
        {"name": label, "number": f"{i:02d}", "caption": "Tools in my toolkit", "items": items}
        for i, (label, items) in enumerate(groups.items(), 1)
    ]


def home(request):
    projects = project_data()
    certs = [{"title": x.title, "issuer": x.issuer, "date": x.issued_date,
              "image": x.image.url if x.image else "", "url": x.credential_url}
             for x in Certificate.objects.all()]
    activities = [{"title": x.title, "category": x.category, "description": x.description,
                   "date": x.date, "image": x.image.url if x.image else ""}
                  for x in Activity.objects.all()]
    exp = list(Experience.objects.all())
    return render(request, "portofolio/home.html", {
        "profile": profile_data(), "projects": projects, "project_count": len(projects),
        "skill_groups": skill_data(), "certificates": certs, "activities": activities,
        "experiences": exp, "certificate_slots": ["Sertifikat 01", "Sertifikat 02", "Sertifikat 03"],
        "activity_slots": ["Kegiatan 01", "Kegiatan 02", "Kegiatan 03"],
    })


def projects(request):
    return redirect("/#projects")


def about(request):
    return redirect("/#about")


def contact(request):
    return redirect("/#contact")


@require_POST
def send_message(request):
    # Honeypot: silent decline for automated spam; no email is claimed to be sent.
    if request.POST.get("website", "").strip():
        return redirect("/#contact")
    name = request.POST.get("name", "").strip()[:120]
    email = request.POST.get("email", "").strip()[:254]
    subject = request.POST.get("subject", "").strip()[:160]
    content = request.POST.get("message", "").strip()[:5000]
    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "Alamat email belum valid. Silakan periksa kembali.")
        return redirect("/#contact")
    if len(name) < 2 or len(subject) < 3 or len(content) < 10:
        messages.error(request, "Lengkapi nama, subjek, dan pesan (minimal 10 karakter).")
        return redirect("/#contact")
    ContactMessage.objects.create(name=name, email=email, subject=subject, message=content)
    messages.success(request, "Pesan tersimpan dan dapat dibaca oleh pemilik melalui admin SenDev.")
    return redirect("/#contact")
