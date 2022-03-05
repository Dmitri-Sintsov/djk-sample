"""djk_sample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import include, re_path
# from django.contrib import admin

from django_jinja_knockout.urls import UrlPath

from djk_sample.views import renderer_test, UserChangeView
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
    ManufacturerFkWidgetGrid, ProfileFkWidgetGrid, TagFkWidgetGrid
)
from event_app.views_ajax import UserFkWidgetGrid

urlpatterns = [
    # re_path(r'^admin/', include(admin.site.urls)),
]

# Allauth views.
if settings.ALLAUTH_DJK_URLS:
    # More pretty-looking bootstrap forms but possibly are not compatible with arbitrary allauth version:
    urlpatterns.append(
        re_path(r'^accounts/', include('django_jinja_knockout._allauth.urls'))
    )
else:
    # Standard allauth DTL templates working with Jinja2 templates via {% load jinja %} template tag library.
    urlpatterns.append(
        re_path(r'^accounts/', include('allauth.urls'))
    )

urlpatterns += [
    re_path(
        r'^renderer-test/$', renderer_test, name='renderer_test',
        kwargs={'view_title': 'Renderer test', 'allow_anonymous': True}),

    UrlPath(UserChangeView)('user_change'),

    # Club
    re_path(
        r'^$', main_page, name='club_main_page',
        kwargs={'view_title': 'Main page', 'allow_anonymous': True}),
    UrlPath(ClubCreate)(name='club_create'),
    # r'^club-create/$'
    UrlPath(ClubCreate)(
        name='club_create_perms_check',
        kwargs={'view_title': 'Add new club with Django permissions check', 'permission_required': 'club_app.add_club'}
    ),
    UrlPath(ClubCreateDTL)(
        name='club_create_dtl',
        kwargs={'view_title': 'Add new club (Django Template Language)'}
    ),
    UrlPath(ClubUpdate)(
        name='club_update',
        args=['club_id'],
        kwargs={'view_title': 'Edit club "{}"'}
    ),
    UrlPath(ClubDetail)(
        name='club_detail',
        args=['club_id'],
        kwargs={'view_title': '{}'}
    ),
    # r'^club-detail-(?P<club_id>\d+)/$'
    UrlPath(ClubList)(
        name='club_list',
        kwargs={'view_title': 'List of sport clubs', 'allow_anonymous': True}
    ),
    UrlPath(ClubListWithComponent)(
        name='club_list_with_component',
        kwargs={'view_title': 'List of sport clubs with their members as GridDialog component'}
    ),
    UrlPath(ClubListDTL)(
        name='club_list_dtl',
        kwargs={'view_title': 'List of sport clubs (Django Template Language)', 'allow_anonymous': True}
    ),

    # Event / Action. Namespace urls resolving test.
    re_path(r'^action-', include('event_app.urls', namespace='action')),

    # Equipment
    UrlPath(EquipmentDetail)(
        name='equipment_detail',
        args=['equipment_id'],
        kwargs={'view_title': '{}'}
    ),
    UrlPath(EquipmentGrid)('equipment_grid', kwargs={'view_title': 'Grid with the available equipment'}),

    # Member
    UrlPath(MemberDetail)(
        name='member_detail',
        args=['member_id'],
        kwargs={'view_title': '{}'}
    ),

    # Foreign key widgets.
    UrlPath(UserFkWidgetGrid)(
        name='user_fk_widget'
        # kwargs={'permission_required': 'auth.change_user'}),
    ),
    UrlPath(ManufacturerFkWidgetGrid)(
        name='manufacturer_fk_widget',
        # kwargs={'permission_required': 'club_app.change_manufacturer'}),
    ),
    UrlPath(ProfileFkWidgetGrid)(
        name='profile_fk_widget',
        # kwargs={'permission_required': 'club_app.change_profile'}),
    ),
    UrlPath(TagFkWidgetGrid)(
        name='tag_fk_widget',
        # kwargs={'permission_required': 'club_app.change_tag'}),
    ),

    # AJAX grids.
    # Sport club.
    UrlPath(SimpleClubGrid)(
        name='club_grid_simple',
        kwargs={'view_title': 'Simple club grid'},
    ),
    UrlPath(SimpleClubGridDTL)(
        name='club_grid_simple_dtl',
        kwargs={'view_title': 'Simple club grid (Django Template Language)'}
    ),
    UrlPath(EditableClubGrid)(
        name='club_grid_editable',
        # kwargs={'view_title': 'Editable club grid', 'permission_required': 'club_app.change_club'}),
        kwargs={'view_title': 'Editable club grid'}
    ),
    UrlPath(ClubGridRawQuery)(
        name='club_grid_raw_query',
        kwargs={'view_title': 'Club grid raw query'}
    ),
    UrlPath(ClubGridWithVirtualField)(
        name='club_grid_with_virtual_field',
        kwargs={'view_title': 'Club grid with virtual field'}
    ),
    UrlPath(ClubGridWithActionLogging)(
        name='club_grid_with_action_logging',
        kwargs={'view_title': 'Club grid with virtual field'}
    ),
    UrlPath(ClubEquipmentGrid)(
        name='club_equipment_grid',
        kwargs={'view_title': 'Club equipment grid'}
    ),

    # Sport club member.
    UrlPath(MemberGrid)(
        name='member_grid',
        kwargs={'view_title': 'Club members grid'}
    ),
    UrlPath(MemberGridTabs)(
        name='member_grid_tabs',
        kwargs={'view_title': 'Club members grid with custom layout'}
    ),
    UrlPath(MemberGridCustomActions)(
        name='member_grid_custom_actions',
        kwargs={'view_title': 'Club members grid with custom actions'}
    ),
    # r'^member-grid-custom-actions(?P<action>/?\w*)/$'
    UrlPath(ClubMemberGrid)(
        name='club_member_grid',
        args=['club_id'],
        kwargs={'view_title': '"{}" members'}
    ),
    # UrlPath generated path:
    # re_path(r'^club-member-grid-(?P<club_id>\w*)(?P<action>/?\w*)/$', ClubMemberGrid.as_view(), name='club_member_grid'),
]

js_info_dict = {
    'domain': 'djangojs',
    'packages': ['django_jinja_knockout', 'djk_sample'],
}

try:
    from django.views.i18n import JavaScriptCatalog
    urlpatterns.append(
        re_path(r'^jsi18n/$', JavaScriptCatalog.as_view(**js_info_dict), name='javascript-catalog'),
    )
except ImportError:
    from django.views.i18n import javascript_catalog
    urlpatterns.append(
        re_path(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog')
    )

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
