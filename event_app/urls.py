from django.urls import re_path


from .views import ActionList
from .views_ajax import ActionGrid


app_name = 'event_app'


urlpatterns = [

    re_path(
        r'^list/$', ActionList.as_view(), name='list',
        kwargs={'view_title': 'Log of actions'}),
    ActionGrid.url_path(
        name='grid',
        kwargs={'view_title': 'Grid with the list of performed actions'}
    ),
]
