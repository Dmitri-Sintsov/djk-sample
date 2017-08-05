"""djk_sample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
# from django.contrib import admin

from djk_sample.views import UserChangeView
from club_app.views import (
    ClubCreate, ClubCreateDTL, ClubUpdate, ClubDetail,
    ClubList, ClubListWithComponent, ClubListDTL,
    EquipmentDetail, MemberDetail
)
from club_app.views import main_page
from club_app.views_ajax import (
    SimpleClubGrid, SimpleClubGridDTL, EditableClubGrid, ClubGridRawQuery,
    ClubGridWithVirtualField, ClubGridWithActionLogging,
    ClubEquipmentGrid, EquipmentGrid,
    MemberGrid, ClubMemberGrid, MemberGridTabs, MemberGridCustomActions,
    ManufacturerFkWidgetGrid, ProfileFkWidgetGrid
)
from event_app.views import ActionList
from event_app.views_ajax import UserFkWidgetGrid, ActionGrid

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
]

# Allauth views.
if settings.ALLAUTH_DJK_URLS:
    # More pretty-looking bootstrap forms but possibly are not compatible with arbitrary allauth version:
    urlpatterns.append(
        url(r'^accounts/', include('django_jinja_knockout._allauth.urls'))
    )
else:
    # Standard allauth DTL templates working with Jinja2 templates via {% load jinja %} template tag library.
    urlpatterns.append(
        url(r'^accounts/', include('allauth.urls'))
    )

urlpatterns += [
    # Class-based views.
    url(r'^user-change(?P<action>/?\w*)/$', UserChangeView.as_view(), name='user_change'),

    # Club
    url(r'^$', main_page, name='club_main_page',
        kwargs={'view_title': 'Main page', 'allow_anonymous': True}),
    url(r'^club-create/$', ClubCreate.as_view(), name='club_create',
        kwargs={'view_title': 'Add new club'}),
    url(r'^club-create-perms-check/$', ClubCreate.as_view(), name='club_create_perms_check',
        kwargs={'view_title': 'Add new club with Django permissions check', 'permission_required': 'club_app.add_club'}),
    url(r'^club-create-dtl/$', ClubCreateDTL.as_view(), name='club_create_dtl',
        kwargs={'view_title': 'Add new club (Django Template Language)'}),
    url(r'^club-update-(?P<club_id>\d+)/$', ClubUpdate.as_view(), name='club_update',
        kwargs={'view_title': 'Edit club "{}"'}),
    url(r'^club-detail-(?P<club_id>\d+)/$', ClubDetail.as_view(), name='club_detail',
        kwargs={'view_title': '{}'}),
    url(r'^club-list/$', ClubList.as_view(), name='club_list',
        kwargs={'view_title': 'List of sport clubs', 'allow_anonymous': True}),
    url(r'^club-list-with-component/$', ClubListWithComponent.as_view(), name='club_list_with_component',
        kwargs={'view_title': 'List of sport clubs with their members as App.GridDialog component'}),
    url(r'^club-list-dtl/$', ClubListDTL.as_view(), name='club_list_dtl',
        kwargs={'view_title': 'List of sport clubs (Django Template Language)', 'allow_anonymous': True}),

    # Action
    url(r'^action-list/$', ActionList.as_view(), name='action_list',
        kwargs={'view_title': 'Log of actions'}),
    url(r'^action-grid(?P<action>/?\w*)/$', ActionGrid.as_view(), name='action_grid',
        kwargs={'view_title': 'Grid with the list of performed actions'}),

    # Equipment
    url(r'^equipment-detail-(?P<equipment_id>\d+)/$', EquipmentDetail.as_view(), name='equipment_detail',
        kwargs={'view_title': '{}'}),
    url(r'^equipment-grid(?P<action>/?\w*)/$', EquipmentGrid.as_view(), name='equipment_grid',
        kwargs={'view_title': 'Grid with the available equipment'}),

    # Member
    url(r'^member-detail-(?P<member_id>\d+)/$', MemberDetail.as_view(), name='member_detail',
        kwargs={'view_title': '{}'}),

    # Foreign key widgets.
    url(r'^user-fk-widget-grid(?P<action>/?\w*)/$', UserFkWidgetGrid.as_view(),
        name='user_fk_widget_grid',
        # kwargs={'ajax': True, 'permission_required': 'auth.change_user'}),
        kwargs={'ajax': True}),
    url(r'^manufacturer-fk-widget-grid(?P<action>/?\w*)/$', ManufacturerFkWidgetGrid.as_view(),
        name='manufacturer_fk_widget_grid',
        # kwargs={'ajax': True, 'permission_required': 'club_app.change_manufacturer'}),
        kwargs={'ajax': True}),
    url(r'^profile-fk-widget-grid(?P<action>/?\w*)/$', ProfileFkWidgetGrid.as_view(),
        name='profile_fk_widget_grid',
        # kwargs={'ajax': True, 'permission_required': 'club_app.change_profile'}),
        kwargs={'ajax': True}),

    # AJAX grids.
    # Sport club.
    url(r'^club-grid-simple(?P<action>/?\w*)/$', SimpleClubGrid.as_view(), name='club_grid_simple',
        kwargs={'view_title': 'Simple club grid'}),
    url(r'^club-grid-simple-dtl(?P<action>/?\w*)/$', SimpleClubGridDTL.as_view(), name='club_grid_simple_dtl',
        kwargs={'view_title': 'Simple club grid (Django Template Language)'}),
    url(r'^club-grid-editable(?P<action>/?\w*)/$', EditableClubGrid.as_view(), name='club_grid_editable',
        # kwargs={'view_title': 'Editable club grid', 'permission_required': 'club_app.change_club'}),
        kwargs={'view_title': 'Editable club grid'}),
    url(r'^club-grid-raw-query(?P<action>/?\w*)/$', ClubGridRawQuery.as_view(), name='club_grid_raw_query',
        kwargs={'view_title': 'Club grid raw query'}),
    url(r'^club-grid-with-virtual-field(?P<action>/?\w*)/$', ClubGridWithVirtualField.as_view(), name='club_grid_with_virtual_field',
        kwargs={'view_title': 'Club grid with virtual field'}),
    url(r'^club-grid-with-action-logging(?P<action>/?\w*)/$', ClubGridWithActionLogging.as_view(),
        name='club_grid_with_action_logging',
        kwargs={'view_title': 'Club grid with virtual field'}),
    url(r'^club-equipment-grid(?P<action>/?\w*)/$', ClubEquipmentGrid.as_view(),
        name='club_equipment_grid',
        kwargs={'view_title': 'Club equipment grid'}),

    # Sport club member.
    url(r'^member-grid(?P<action>/?\w*)/$', MemberGrid.as_view(), name='member_grid',
        kwargs={'view_title': 'Club members grid'}),
    url(r'^member-grid-tabs(?P<action>/?\w*)/$', MemberGridTabs.as_view(), name='member_grid_tabs',
        kwargs={'view_title': 'Club members grid with custom layout'}),
    url(r'^member-grid-custom-actions(?P<action>/?\w*)/$', MemberGridCustomActions.as_view(), name='member_grid_custom_actions',
        kwargs={'view_title': 'Club members grid with custom actions'}),
    url(r'^club-member-grid-(?P<club_id>\w*)(?P<action>/?\w*)/$', ClubMemberGrid.as_view(), name='club_member_grid',
        kwargs={'view_title': '"{}" members'}),
]

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('djk_sample',),
}

try:
    from django.views.i18n import JavaScriptCatalog
    urlpatterns.append(
        url(r'^jsi18n/$', JavaScriptCatalog.as_view(**js_info_dict), name='javascript-catalog'),
    )
except ImportError:
    from django.views.i18n import javascript_catalog
    urlpatterns.append(
        url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog')
    )

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static
    urlpatterns += staticfiles_urlpatterns()
    # media_static = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += media_static
