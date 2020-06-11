from django_jinja_knockout.urls import UrlPath

from .views import ActionList
from .views_ajax import ActionGrid


app_name = 'event_app'


urlpatterns = [

    UrlPath(ActionList)(
        name='list',
        kwargs={'view_title': 'Log of actions'}
    ),
    UrlPath(ActionGrid)(
        name='grid',
        kwargs={'view_title': 'Grid with the list of performed actions'}
    ),
]
