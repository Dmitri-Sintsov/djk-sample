from django.conf.urls import url


from .views import ActionList
from .views_ajax import ActionGrid


app_name = 'event_app'


urlpatterns = [

    url(r'^list/$', ActionList.as_view(), name='list',
        kwargs={'view_title': 'Log of actions'}),
    url(r'^grid(?P<action>/?\w*)/$', ActionGrid.as_view(), name='grid',
        kwargs={'view_title': 'Grid with the list of performed actions'}),
]
