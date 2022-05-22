'use rollup'

import { vmRouter } from '../../djk/js/ioc.js';
import { documentReadyHooks, startApp } from '../../djk/js/document.js';
import { ClosablePopover, ButtonPopover, ContentPopover } from '../../djk/js/popover.js';
import { UiPopover } from '../../djk/js/ui.js';

documentReadyHooks.push(function() {

    var closablePopover = new ClosablePopover({target: '#input-inline-closable-popover'});
    var buttonPopover = new ButtonPopover({target: '#input-inline-button-popover'});
    vmRouter.respond([
        {
            'view': 'tooltip_error',
            'selector': '#input-tooltip-error',
            'title': 'Error title',
            'messages': ['Tooltip error message1', 'Tooltip error message2'],
        },
        {
            'view': 'popover_error',
            'selector': '#input-popover-error',
            'title': 'Error title',
            'messages': ['Popover error message1', 'Popover error message2'],
        },
    ]);
    $('#empty_popover_button').on('click', function() {
        $('[bs-toggle="popover"]').each(function() {
            new UiPopover(this).empty();
        });
    });
    $('#update_popover_button').on('click', function() {
        $('[bs-toggle="popover"]').each(function() {
            new UiPopover(this).update({
                content: 'Show again!'
            });
        });
    });
    $('#dispose_popovers_button').on('click', function() {
        $('[bs-toggle="popover"]').each(function() {
            new UiPopover(this).dispose();
        });
        closablePopover.destroy();
        buttonPopover.destroy();
    });

});

startApp();
