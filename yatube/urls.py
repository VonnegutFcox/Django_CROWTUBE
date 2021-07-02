# yatube\urls.py
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404, handler500
# эти строки — в начало файла, рядом с импортом других модулей
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings

handler404 = "posts.views.page_not_found" # noqa
handler500 = "posts.views.server_error" # noqa


urlpatterns = [
    #  регистрация и авторизация
    path("auth/", include("users.urls")),

    #  если нужного шаблона для /auth не нашлось в файле users.urls —
    #  ищем совпадения в файле django.contrib.auth.urls
    path("auth/", include("django.contrib.auth.urls")),

    #  раздел администратора
    path("admin/", admin.site.urls),

    #  обработчик для главной страницы ищем в urls.py приложения posts
    path("", include("posts.urls", namespace='posts')),

    path('about/', include('about.urls', namespace='about')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

