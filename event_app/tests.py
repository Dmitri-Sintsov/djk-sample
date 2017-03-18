from django_jinja_knockout.viewmodels import to_json
from django_jinja_knockout.automation import AutomationCommands


class EventAppCommands(AutomationCommands):

    event_list_navigate = (
        'click_anchor_by_view', {'viewname': 'action_list'},
        'click_anchor_by_view', (
            'action_list',
            {},
            {
                'page': 2,
            }
        ),
        'click_anchor_by_view', (
            'action_list',
            {},
            {
                'list_filter': to_json({
                    'action_type': 0,
                })
            }
        ),
        'click_anchor_by_view', (
            'action_list',
            {},
            {
                'list_filter': to_json({
                    'action_type': 0,
                }),
                'page': 3,
            }
        ),
        'click_by_link_text', ('Sport club member',),
    )

    event_list_preview_member = (
        'click_anchor_by_view', (
            'member_detail',
            {
                'member_id': 2,
            },
        ),
        'button_click', ('Read',),
        'dialog_button_click', ('OK',),
    )
