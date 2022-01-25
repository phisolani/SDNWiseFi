from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'sdn'
urlpatterns = [
    # Main url
    path('', login_required(views.IndexView.as_view()), name='index'),

    # Resources urls
    path('resources/tenant/', login_required(views.TenantView.as_view()), name='tenant-view'),
    path('resources/tenant/new/', login_required(views.TenantCreate.as_view()), name='tenant-new'),
    path('resources/tenant/update/<int:pk>/', login_required(views.TenantUpdate.as_view()), name='tenant-update'),
    path('resources/tenant/delete/<int:pk>/', login_required(views.TenantDelete.as_view()), name='tenant-delete'),

    path('resources/controller/', login_required(views.ControllerView.as_view()), name='controller-view'),
    path('resources/controller/new/', login_required(views.ControllerCreate.as_view()), name='controller-new'),
    path('resources/controller/update/<int:pk>/', login_required(views.ControllerUpdate.as_view()), name='controller-update'),
    path('resources/controller/delete/<int:pk>/', login_required(views.ControllerDelete.as_view()), name='controller-delete'),

    path('resources/graph/', login_required(views.GraphView.as_view()), name='graph-view'),
    path('resources/graph/new/', login_required(views.GraphCreate.as_view()), name='graph-new'),
    path('resources/graph/update/<int:pk>/', login_required(views.GraphUpdate.as_view()), name='graph-update'),
    path('resources/graph/delete/<int:pk>/', login_required(views.GraphDelete.as_view()), name='graph-delete'),

    # Visualization urls
    path('visualization/tenant/', login_required(views.TenantSelectView.as_view()), name='tenant-select'),
    path('visualization/tenant/<int:pk>/', login_required(views.DataPlaneView.as_view()), name='tenant-visualization'),
    path('visualization/tenant/<int:tenant_id>/data/', login_required(views.tenant_data), name='tenant-data'),
    path('visualization/tenant/<int:tenant_id>/set_slice/', login_required(views.send_slice_config), name='tenant-slice-config'),
    path('visualization/tenant/<int:tenant_id>/set_mcda/', login_required(views.send_mcda_config), name='tenant-mcda-config'),
    path('visualization/tenant/<int:tenant_id>/set_adaptive_slicing/', login_required(views.send_adaptive_slicing_config), name='tenant-adaptive-slicing-config'),
]