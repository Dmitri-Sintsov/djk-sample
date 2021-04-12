'use rollup'

import { inherit } from '../djk/js/dash.js';
import { TabPane } from '../djk/js/tabpane.js';
import { Actions } from '../djk/js/actions.vm.js';
import { GridActions } from '../djk/js/grid/actions.vm.js';
import { Grid } from '../djk/js/grid.js';
import { globalIoc } from '../djk/js/ioc.js';
import { startApp } from '../djk/js/document.js';


/**
 * This code is partially shared between these templates / class-based views
 *
 * 'club_grid_with_action_logging.htm' / club_app.views_ajax.ClubGridWithActionLogging
 * 'club_equipment.htm' / club_app.views_ajax.ClubEquipmentGrid
 *
 */
function ClubGridActions(options) {
    inherit(GridActions.prototype, this);
    inherit(Actions.prototype, this);
    this.init(options);
};

(function(ClubGridActions) {

    ClubGridActions.updateDependentGrid = function(selector) {
        // Get instance of dependent grid.
        var grid = $(selector).component();
        if (grid !== null) {
            // Update dependent grid.
            grid.actions.perform('update');
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
        // Get client-side class of EquipmentGrid component by id (instance of Grid or derived class).
        var equipmentGrid = $('#equipment_grid').component();
        if (equipmentGrid !== null) {
            // Update rows of MemberGrid component (instance of Grid or derived class).
            equipmentGrid.updatePage(equipmentGridView);
            // Highlight equipment tab so the user will know it has updated list page.
            TabPane().highlight('#equipment_tab');
            // Switch to equipment grid tab to show equipment changes.
            // window.location.hash = '#equipment_tab';
        }
    };

})(ClubGridActions.prototype);


function ClubGrid(options) {
    inherit(Grid.prototype, this);
    this.init(options);
};

(function(ClubGrid) {

    ClubGrid.iocGridActions = function(options) {
        return new ClubGridActions(options);
    };

})(ClubGrid.prototype);

globalIoc.add('ClubGrid', function(options) {
    return new ClubGrid(options);
});

startApp();
