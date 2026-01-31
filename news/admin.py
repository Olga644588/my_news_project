from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Scope, Tag



class ScopeInlineFormSet(BaseInlineFormSet):
    def clean(self):
        main_count = 0
        tag_ids = set()

        for form in self.forms:
            if not form.is_valid() or form.cleaned_data.get('DELETE'):
                continue

            is_main = form.cleaned_data.get('is_main')
            tag = form.cleaned_data.get('tag')

            if is_main:
                main_count += 1
            if tag:
                if tag.id in tag_ids:
                    raise ValidationError(f'Тег "{tag.name}" указан дважды. Удалите дубликат.')
                tag_ids.add(tag.id)

        if main_count == 0:
            raise ValidationError('Необходимо выбрать один основной раздел (is_main).')
        if main_count > 1:
            raise ValidationError('Можно выбрать только один основной раздел (is_main).')


        return super().clean()

class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormSet
    extra = 1
    fields = ('tag', 'is_main')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tag":
            kwargs["queryset"] = Tag.objects.all().order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['is_main'].widget.attrs['class'] = 'is-main-checkbox'
        return formset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    list_display = ['title', 'published_at']
    search_fields = ['title']

    class Media:
        css = {
            'all': ('admin/css/custom.css',)
        }

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
