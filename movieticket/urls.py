urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tickets.urls')),
]


