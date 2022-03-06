'use rollup'

import { inherit } from '../../djk/js/dash.js';
import { Dialog } from '../../djk/js/dialog.js';
import { ActionTemplateDialog } from '../../djk/js/modelform.js';
import { ui } from '../../djk/js/ui.js';
import { Actions } from '../../djk/js/actions.js';
import { GridActions } from '../../djk/js/grid/actions.js';
import { GridRow } from '../../djk/js/grid/row.js';
import { Grid } from '../../djk/js/grid.js';

import { componentIoc } from '../../djk/js/ioc.js';
import { startApp } from '../../djk/js/document.js';

import { Url } from '../../djk/js/url.js';

function MemberGridRow(options) {
    inherit(GridRow.prototype, this);
    this.init(options);
};

(function(MemberGridRow) {

    MemberGridRow.useInitClient = true;

    MemberGridRow.display = function(field) {
        var displayValue = this._super._call('display', field);
        switch (field) {
        case 'role':
            // Display field value as bootstrap label.
            var types = ['success', 'info', 'primary'];
            displayValue = $('<span>', {
                'class': ui.labelClass + ' preformatted'
            })
            .text(displayValue)
            .addClass(
                ui.labelClass + '-' + (this.values[field] < types.length ? types[this.values[field]] : 'info')
            );
            break;
        case 'note':
            // Display field value as bootstrap clickable popover.
            var gridColumnOrder = this.ownerGrid.getKoGridColumn(field).order;
            if (this.values[field] !== '') {
                displayValue = $('<button>', {
                    'class': 'btn btn-info',
                    'data-content': this.values[field],
                    'data-toggle': 'popover',
                    'data-html': false,
                    'data-trigger': 'click',
                    'data-placement': 'bottom',
                    'title': gridColumnOrder.name,
                }).text('Full text');
            }
            break;
        case 'is_endorsed':
            // Display field value as form input.
            var attrs = {
                'type': 'checkbox',
                'class': 'form-field club-member',
                'data-pkval': this.getValue(this.ownerGrid.meta.pkField),
                'name': field + '[]',
            };
            if (this.values[field]) {
                attrs['checked'] = 'checked';
            }
            displayValue = $('<input>', attrs);
        }
        return displayValue;
    };

    MemberGridRow.hasEnabledAction = function(action) {
        if (action.name === 'quick_endorse' && this.values['is_endorsed'] === true) {
            return false;
        }
        if (action.name === 'quick_disendorse' && this.values['is_endorsed'] === false) {
            return false;
        }
        return true;
    };

})(MemberGridRow.prototype);


function MemberGridActions(options) {
    inherit(GridActions.prototype, this);
    inherit(Actions.prototype, this);
    this.init(options);
};

(function(MemberGridActions) {

    // Generates data for AJAX call.
    MemberGridActions.queryargs_endorse_members = function(queryArgs) {
        queryArgs['member_ids'] = JSON.stringify(this.grid.getEndorsedMemberIds());
        return queryArgs;
    };

    MemberGridActions.callback_endorse_members = function(viewModel) {
        this.grid.updatePage(viewModel);
        if (viewModel.update_rows.length > 0) {
            var vm = {
                title: 'Changed member endorsements',
                description: viewModel.description
            };
            this.renderDescription(vm);
        } else {
            var vm = {
                'title': 'No membership was changed',
                'message': 'Please invert some checkbox first.'
            };
        }
        // this.grid.updateMeta(viewModel.meta);
        new Dialog(vm).alert();
    };

    MemberGridActions.callback_quick_endorse = function(viewModel) {
        this.grid.updatePage(viewModel);
    };

    MemberGridActions.callback_quick_disendorse = function(viewModel) {
        this.grid.updatePage(viewModel);
    };

    // Client-side invocation of the action.
    MemberGridActions.perform_edit_note = function(queryArgs, ajaxCallback) {
        var actionDialog = new ActionTemplateDialog({
            template: 'member_note_form',
            owner: this.grid,
            meta: {
                noteLabel: 'Member note',
                note: this.grid.lastClickedKoRow.getValue('note')
            },
        });
        actionDialog.show();
    };

    MemberGridActions.callback_edit_note = function(viewModel) {
        this.grid.updatePage(viewModel);
    };

})(MemberGridActions.prototype);


function MemberGrid(options) {
    inherit(Grid.prototype, this);
    this.init(options);
};

(function(MemberGrid) {

    // An example to use outer module Url() call in knockout bindings:
    MemberGrid.getUrl = function(route, kwargs) {
        return Url(route, kwargs);
    };

    MemberGrid.iocRow = function(options) {
        return new MemberGridRow(options);
    };

    MemberGrid.iocGridActions = function(options) {
        return new MemberGridActions(options);
    };

    MemberGrid.getEndorsedMemberIds = function() {
        var members = {};
        $('input.club-member[name^="is_endorsed"]')
        .map(function() {
            members[$(this).data('pkval')] = $(this).prop('checked');
        });
        return members;
    };

    MemberGrid.onChangeEndorsement = function(data, ev) {
        this.actions.perform('endorse_members');
    };

})(MemberGrid.prototype);

componentIoc.add('MemberGrid', function(options) {
    return new MemberGrid(options);
});

startApp();
