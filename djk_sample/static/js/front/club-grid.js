/**
 * This code is partially shared between these templates / class-based views
 *
 * 'club_grid_with_action_logging.htm' / club_app.views_ajax.ClubGridWithActionLogging
 * 'club_equipment.htm' / club_app.views_ajax.ClubEquipmentGrid
 *
 */
App.ClubGridActions = function(options) {
    $.inherit(App.GridActions.prototype, this);
    $.inherit(App.Actions.prototype, this);
    this.init(options);
};

(function(ClubGridActions) {

    ClubGridActions.updateDependentGrid = function(selector) {
        // Get instance of dependent grid.
        var grid = $(selector).component();
        if (grid !== null) {
            // Update dependent grid.
            grid.gridActions.perform('update');
        }
    };

    // Used in club_app.views_ajax.ClubGridWithActionLogging.
    ClubGridActions.callback_save_inline = function(viewModel) {
        this._super._call('callback_save_form', viewModel);
        this.updateDependentGrid('#action_grid');
        this.updateDependentGrid('#equipment_grid');
    };

    // Used in club_app.views_ajax.ClubEquipmentGrid.
    ClubGridActions.callback_save_form = function(viewModel) {
        this._super._call('callback_save_form', viewModel);
        this.updateDependentGrid('#action_grid');
        this.updateDependentGrid('#equipment_grid');
    };

    ClubGridActions.callback_delete_confirmed = function(viewModel) {
        this._super._call('callback_delete_confirmed', viewModel);
        this.updateDependentGrid('#action_grid');
        this.updateDependentGrid('#equipment_grid');
    };

    ClubGridActions.callback_add_equipment = function(viewModel) {
        this.callback_create_form(viewModel);
    };

    ClubGridActions.callback_save_equipment = function(viewModel) {
        var equipmentGridView = viewModel.equipment_grid_view;
        delete viewModel.equipment_grid_view;
        this.grid.updatePage(viewModel);
        // Get client-side class of EquipmentGrid component by id (instance of App.ko.Grid or derived class).
        var equipmentGrid = $('#equipment_grid').component();
        if (equipmentGrid !== null) {
            // Update rows of MemberGrid component (instance of App.ko.Grid or derived class).
            equipmentGrid.updatePage(equipmentGridView);
            // Highlight equipment tab so the user will know it has updated list page.
            App.TabPane.highlight('#equipment_tab');
            // Switch to equipment grid tab to show equipment changes.
            // window.location.hash = '#equipment_tab';
        }
    };

})(App.ClubGridActions.prototype);


App.ko.ClubGrid = function(options) {
    $.inherit(App.ko.Grid.prototype, this);
    this.init(options);
};

(function(ClubGrid) {

    ClubGrid.iocGridActions = function(options) {
        return new App.ClubGridActions(options);
    };

})(App.ko.ClubGrid.prototype);
