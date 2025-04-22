from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.users.urls")),
]


urlpatterns += [
    path("api/", include("apps.transactions.urls")),
]


urlpatterns += [
    path("api/dashboard/", include("apps.dashboard.urls")),
]


urlpatterns += [
    path("api/", include("apps.category.urls")),
]

urlpatterns += [
    path("api/", include("apps.budget.urls")),
]

urlpatterns += [
    path("api/report/", include("apps.reports.urls")),
]
