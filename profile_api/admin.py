from django.contrib import admin

from profile_api.models import Teacher, Category, Gender, Reviews, Student


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ['id', 'gender']

    def has_add_permission(self, request):
        gender_count = Gender.objects.all().count()
        if gender_count >= 2:
            return False
        else:
            return True


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass
