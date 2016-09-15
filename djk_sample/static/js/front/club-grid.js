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
            actionGrid.gridActions.perform('update');
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

    ClubGridActions.queryargs_endorse_all_members = function(options) {
        var memberGrid = $('#member_grid').component();
        var visibleMembersPkVals = _.map(memberGrid.gridRows(), function(gridRow) {
            return gridRow.getValue(memberGrid.meta.pkField);
        });
        options['visibleMembersPkVals'] = memberGridPkVals;
    };

    ClubGridActions.callback_endorse_all_members = function(viewModel) {
        var memberGridView = viewModel.member_grid_view;
        delete viewModel.member_grid_view;

        this.grid.updatePage(viewModel);
        // Get client-side class of MemberGrid component by id (instance of App.ko.Grid or derived class).
        var memberGrid = $('#member_grid').component();
        if (memberGrid !== null) {
            // Update rows of MemberGrid component (instance of App.ko.Grid or derived class).
            memberGrid.updatePage(memberGridView);
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
