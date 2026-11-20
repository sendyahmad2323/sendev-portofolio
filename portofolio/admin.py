from django.contrib import admin
from .models import Activity, Certificate, ContactMessage, Experience, Project, SiteProfile, Skill


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    list_display = ("brand", "name", "role", "available_for_work")
    fieldsets = (
        ("Brand & perkenalan", {"fields": ("brand", "name", "role", "headline", "tagline", "about", "available_for_work")}),
        ("Upload gambar & CV", {"fields": ("avatar", "about_photo", "resume")}),
        ("Kontak & sosial", {"fields": ("email", "location", "github_url", "linkedin_url", "instagram_url", "whatsapp_url")}),
    )

    def has_add_permission(self, request):
        return not SiteProfile.objects.exists() and super().has_add_permission(request)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "featured", "order", "created_at")
    list_filter = ("category", "featured")
    search_fields = ("title", "tech_stack", "description")
    list_editable = ("featured", "order")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency")
    list_filter = ("category",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("position", "company", "start_date", "current")


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("title", "issuer", "issued_date", "order")
    search_fields = ("title", "issuer")
    list_editable = ("order",)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "date", "order")
    search_fields = ("title", "description")
    list_editable = ("order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")

    def has_add_permission(self, request):
        return False


admin.site.site_header = "SenDev • Content Studio"
admin.site.site_title = "SenDev Admin"
admin.site.index_title = "Kelola konten portofolio"
