App.ClubGridActions = function(options) {
    $.inherit(App.GridActions.prototype, this);
    this.init(options);
};

(function(ClubGridActions) {

    ClubGridActions.updateActionGrid = function() {
        // Get instance of ActionGrid.
        var actionGrid = $('#action_grid').component();
        if (actionGrid !== null) {
            // Update ActionGrid.
            actionGrid.gridActions.perform('list');
        }
    };

    ClubGridActions.callback_save_inline = function(viewModel) {
        this._super._call('callback_save_inline', viewModel);
        this.updateActionGrid();
    };

    ClubGridActions.callback_delete_confirmed = function(viewModel) {
        this._super._call('callback_delete_confirmed', viewModel);
        this.updateActionGrid();
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
