'use strict';

App.ko.MemberGridRow = function(options) {
    $.inherit(App.ko.GridRow.prototype, this);
    this.init(options);
};

(function(MemberGridRow) {

    MemberGridRow.useInitClient = true;

    MemberGridRow.toDisplayValue = function(value, field) {
        var displayValue = this._super._call('toDisplayValue', value, field);
        switch (field) {
        case 'role':
            // Display field value as bootstrap label.
            var types = ['success', 'info', 'primary'];
            displayValue = $('<span>', {
                'class': App.ui.labelClass + ' preformatted'
            })
            .text(displayValue)
            .addClass(
                App.ui.labelClass + '-' + (this.values[field] < types.length ? types[this.values[field]] : 'info')
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

})(App.ko.MemberGridRow.prototype);


App.MemberGridActions = function(options) {
    $.inherit(App.GridActions.prototype, this);
    $.inherit(App.Actions.prototype, this);
    this.init(options);
};

(function(MemberGridActions) {

    // Generates data for AJAX call.
    MemberGridActions.queryargs_endorse_members = function(options) {
        options['member_ids'] = JSON.stringify(this.grid.getEndorsedMemberIds());
        return options;
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
        new App.Dialog(vm).alert();
    };

    MemberGridActions.callback_quick_endorse = function(viewModel) {
        this.grid.updatePage(viewModel);
    };

    MemberGridActions.callback_quick_disendorse = function(viewModel) {
        this.grid.updatePage(viewModel);
    };

    // Client-side invocation of the action.
    MemberGridActions.perform_edit_note = function(queryArgs, ajaxCallback) {
        var actionDialog = new App.ActionTemplateDialog({
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

})(App.MemberGridActions.prototype);


App.ko.MemberGrid = function(options) {
    $.inherit(App.ko.Grid.prototype, this);
    this.init(options);
};

(function(MemberGrid) {

    MemberGrid.iocRow = function(options) {
        return new App.ko.MemberGridRow(options);
    };

    MemberGrid.iocGridActions = function(options) {
        return new App.MemberGridActions(options);
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

})(App.ko.MemberGrid.prototype);
