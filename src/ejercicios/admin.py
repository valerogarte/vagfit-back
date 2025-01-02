from django.contrib import admin
from .models import Ejercicio, Equipamiento, Musculo
from django.utils.safestring import mark_safe

class SortedRelatedFieldListFilter(admin.RelatedFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_choices = sorted(self.lookup_choices, key=lambda x: x[1])

class EjercicioAdmin(admin.ModelAdmin):
    search_fields = [
        'nombre',
        'equipamiento__titulo',
        'musculo_primario__titulo',
        'musculo_secundario__titulo',
    ]
    list_filter = [
        ('equipamiento', SortedRelatedFieldListFilter),
        ('musculo_primario', SortedRelatedFieldListFilter),
        ('musculo_secundario', SortedRelatedFieldListFilter),
    ]
    list_display = ('imagen_thumb', 'nombre', 'musculo_primario', 'equipamiento', 'realizar_por_extremidad')
    list_editable = ('musculo_primario', 'equipamiento')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('nombre')

    def imagen_thumb(self, obj):
        if obj.imagen_uno and obj.imagen_dos:
            return mark_safe(f'''
                <div>
                    <img id="img-{obj.id}" src="{obj.imagen_uno.url}" style="width: auto; height: auto; max-width: 200px; max-height: 150px;" />
                    <script>
                        (function() {{
                            var imgElement = document.getElementById("img-{obj.id}");
                            var images = ["{obj.imagen_uno.url}", "{obj.imagen_dos.url}"];
                            var index = 0;
                            setInterval(function() {{
                                index = (index + 1) % images.length;
                                imgElement.src = images[index];
                            }}, 1000);
                        }})();
                    </script>
                </div>
            ''')
        elif obj.imagen_uno:
            return mark_safe(f'<img src="{obj.imagen_uno.url}" style="width: auto; height: auto; max-width: 200px; max-height: 150px;" />')
        return "-"
    imagen_thumb.short_description = 'Imagen'


admin.site.register(Ejercicio, EjercicioAdmin)
admin.site.register(Equipamiento)
admin.site.register(Musculo)