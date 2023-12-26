from django.urls import include, path
from classroom import views
from django.contrib import admin
from classroom import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('vendor_login/', views.vendor_login, name='vendor_login'),
    path('user_login/', views.user_login, name='user_login'),
    path('signup/', views.signup, name='signup'),
    path('edit/<int:firmware_id>/', views.edit_firmware, name='edit_firmware'),
    path('delete/<int:firmware_id>/',views. delete_firmware, name='delete_firmware'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_Firmware/', views.add_Firmware, name='add_Firmware'),
    path('save_record/', views.save_record, name='save_record'),
    path('logout/', views.logout_view, name='logout'),
    path('firmware_records/', views.firmware_records, name='firmware_records'),
    path('Record/', views.Record.as_view(), name='Record'),
    path('users/', views.UserView.as_view(), name='users'),
    path('view_record/<int:pk>', views.recordReadView.as_view(), name='view_record'),
    path('view_record1/<int:pk>', views.record1ReadView.as_view(), name='view_record1'),
    path('view_user/<int:pk>', views.UserReadView.as_view(), name='view_user'),
    path('update_record/<int:pk>', views.recordUpdateView.as_view(), name='update_record'),
    path('update_car/<int:pk>', views.CarUpdateView.as_view(), name='update_car'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('delete_car1/<int:pk>', views.record1DeleteView.as_view(), name='delete_record1'),
    path('user_update/<int:pk>', views.UserUpdateView.as_view(), name='user_update'),
    path('delete_user/<int:pk>', views.DeleteUser.as_view(), name='delete_user'),
    path('create/create', views.create, name='create'),






] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
