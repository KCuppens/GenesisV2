$(document).ready(function () {
    $(".row-canvas-draggable").draggable({
        helper: function() {
            return getCanvasRowHTML();
        },
        stop: function (ev, ui) {
            var canvas = $('.canvas-builder').data('id');
            var csrf = $('.canvas-builder').data('csrf');
            $.ajax({
                type: 'POST',
                url: 'canvas-row',
                data: {
                    'canvas': canvas,
                    'action': 'add',
                    'csrfmiddlewaretoken': csrf, 
                },
                success: function(data) {
                    $('.canvas-builder').html(data.template);
                }
            });
        },
        connectToSortable: ".canvas-builder"
    });
    function getOverview() {
        var canvas = $('.canvas-builder').data('id');
        var csrf = $('.canvas-builder').data('csrf');
        $.ajax({
            type: 'POST',
            url: 'canvas-row',
            data: {
                'canvas': canvas,
                'action': 'overview',
                'csrfmiddlewaretoken': csrf, 
            },
            success: function(data) {
                $('.canvas-builder').html(data.template);
            }
        });
    }
    $('.canvas-builder').on('click', '.row-canvas-delete', function(e){
        e.stopPropagation();
        var canvas = $('.canvas-builder').data('id');
        var row = $('.row-canvas-delete').data('id');
        var csrf = $('.canvas-builder').data('csrf');
        var row = $(this).data('id');
        $.ajax({
            type: 'POST',
            url: 'canvas-row',
            data: {
                'canvas': canvas,
                'action': 'delete',
                'row': row,
                'csrfmiddlewaretoken': csrf, 
            },
            success: function(data) {
                $('.canvas-builder').html(data.template);
            }
        });
    });
    $('.canvas-builder').on('click', '.add-block', function(e){
        e.stopPropagation();
        if($(this).parent().hasClass('is-selected')){
            $(this).parent().siblings().removeClass('is-selected');
            $(this).parent().removeClass('is-selected');
        } else {
            $(this).parent().siblings().removeClass('is-selected');
            $(this).parent().addClass('is-selected');
        }
        var colsize = $(this).data('colsize');
        var col = $(this).data('col');
        var csrf = $('.canvas-builder').data('csrf');
        var canvas = $('.canvas-builder').data('id');
        $.ajax({
            type: 'POST',
            url: 'canvas-row',
            data: {
                'csrfmiddlewaretoken': csrf,
                'colsize': colsize,
                'col': col,
                'canvas': canvas,
                'action': 'openmodal'
            },
            success: function (data) {
                $('.overview-blocks').html(data.template);
                $('#exampleModal').modal();
            }
        });
    });

    $('.canvas-builder').on('click', '.col-canvas-replace', function(e){
        var colsize = $(this).data('colsize');
        var col = $(this).data('col');
        var csrf = $('.canvas-builder').data('csrf');
        var canvas = $('.canvas-builder').data('id');
        $.ajax({
            type: 'POST',
            url: 'canvas-row',
            data: {
                'csrfmiddlewaretoken': csrf,
                'colsize': colsize,
                'col': col,
                'canvas': canvas,
                'action': 'openmodal'
            },
            success: function (data) {
                $('.overview-blocks').html(data.template);
                $('#exampleModal').modal();
            }
        });
    });

    function getAjaxForm(block){
        var csrf = $('.canvas-builder').data('csrf');
        $.ajax({
            type: 'POST',
            url: 'canvas-content',
            data: {
                'csrfmiddlewaretoken': csrf,
                'block': block,
            },
            success: function (data) {
                $('.block-content').html(data.template);
            }
        });
    }; 

    $('.canvas-builder').on('click', '.col-canvas-edit', function(e){
        $('#contentModal').modal();
        var block = $(this).data('block');
        getAjaxForm(block);
    });
    
    getOverview();
    $(".canvas-builder").sortable({
        cursor: 'move',
        placeholder: 'placeholder',
        cancel: "span",
    });

    $(".form_builder_area").disableSelection();

    function getCanvasRowHTML() {
        return $('<div>').addClass('row-canvas layout-top-spacing col-md-12');
    }

    function getCol6HTML() {
        return $('<div>').addClass('row-canvas layout-top-spacing col-md-12'); 
    }

    function getCol3HTML() {
        return '<div class="col-md-3 canvas-col"></div><div class="col-md-3 canvas-col"></div><div class="col-md-3 canvas-col"></div><div class="col-md-3 canvas-col"></div>';
    }

    function getCol4HTML() {
        return '<div class="col-md-4 canvas-col"></div><div class="col-md-4 canvas-col"></div><div class="col-md-4 canvas-col"></div>';
    }

    function getCol84HTML() {
        return '<div class="col-md-8 canvas-col"></div><div class="col-md-4 canvas-col"></div>';
    }

    function getCol48HTML() {
        return '<div class="col-md-4 canvas-col"></div><div class="col-md-8 canvas-col"></div>';
    }

    function allElementsFromPoint(x, y) {
        var element, elements = [];
        var old_visibility = [];
        while (true) {
            element = document.elementFromPoint(x, y);
            if (!element || element === document.documentElement) {
                break;
            }
            elements.push(element);
            old_visibility.push(element.style.visibility);
            element.style.visibility = 'hidden'; // Temporarily hide the element (without changing the layout)
        }
        for (var k = 0; k < elements.length; k++) {
            elements[k].style.visibility = old_visibility[k];
        }
        elements.reverse();
        return elements;
    }

    $( ".row-canvas-droppable-6" ).draggable({
        
        helper: function() {
            return getCol6HTML();
        },
        stop: function (ev, ui) {
            var els = allElementsFromPoint(ev.pageX, ev.pageY);
            var row = els[8];
            var canvas = $('.canvas-builder').data('id');
            var csrf = $('.canvas-builder').data('csrf');
            
            $.ajax({
                type: 'POST',
                url: 'canvas-row',
                data: {
                    'canvas': canvas,
                    'row': $(row).data('row'),
                    'action': 'addcolumn',
                    'colblock': "6-6",
                    'csrfmiddlewaretoken': csrf, 
                },
                success: function(data) {
                    $('.canvas-builder').html(data.template);
                }
            });
        },
    });
    $( ".row-canvas-droppable-4" ).draggable({
        
        helper: function() {
            return getCol4HTML();
        },
        stop: function (ev, ui) {
            var els = allElementsFromPoint(ev.pageX, ev.pageY);
            var row = els[8];
            var canvas = $('.canvas-builder').data('id');
            var csrf = $('.canvas-builder').data('csrf');
            
            $.ajax({
                type: 'POST',
                url: 'canvas-row',
                data: {
                    'canvas': canvas,
                    'row': $(row).data('row'),
                    'action': 'addcolumn',
                    'colblock': "4-4-4",
                    'csrfmiddlewaretoken': csrf, 
                },
                success: function(data) {
                    $('.canvas-builder').html(data.template);
                }
            });
        },
        
    });
    $( ".row-canvas-droppable-3" ).draggable({
        
        helper: function() {
            return getCol3HTML();
        },
        stop: function (ev, ui) {
            var els = allElementsFromPoint(ev.pageX, ev.pageY);
            var row = els[8];
            var canvas = $('.canvas-builder').data('id');
            var csrf = $('.canvas-builder').data('csrf');
            
            $.ajax({
                type: 'POST',
                url: 'canvas-row',
                data: {
                    'canvas': canvas,
                    'row': $(row).data('row'),
                    'action': 'addcolumn',
                    'colblock': "3-3-3-3",
                    'csrfmiddlewaretoken': csrf, 
                },
                success: function(data) {
                    $('.canvas-builder').html(data.template);
                }
            });
        },
        
    });
    $( ".row-canvas-droppable-84" ).draggable({
        
        helper: function() {
            return getCol84HTML();
        },
        stop: function (ev, ui) {
            var els = allElementsFromPoint(ev.pageX, ev.pageY);
            var row = els[8];
            var canvas = $('.canvas-builder').data('id');
            var csrf = $('.canvas-builder').data('csrf');
            
            $.ajax({
                type: 'POST',
                url: 'canvas-row',
                data: {
                    'canvas': canvas,
                    'row': $(row).data('row'),
                    'action': 'addcolumn',
                    'colblock': "8-4",
                    'csrfmiddlewaretoken': csrf, 
                },
                success: function(data) {
                    $('.canvas-builder').html(data.template);
                }
            });
        },
    });
    $( ".row-canvas-droppable-48" ).draggable({
        
        helper: function() {
            return getCol48HTML();
        },
        stop: function (ev, ui) {
            var els = allElementsFromPoint(ev.pageX, ev.pageY);
            var row = els.filter(function() {
                return $(this).hasClass('canvas-row');
            });
            var canvas = $('.canvas-builder').data('id');
            var csrf = $('.canvas-builder').data('csrf');
            console.log(els, row);
            $.ajax({
                type: 'POST',
                url: 'canvas-row',
                data: {
                    'canvas': canvas,
                    'row': $(row).data('row'),
                    'action': 'addcolumn',
                    'colblock': "4-8",
                    'csrfmiddlewaretoken': csrf, 
                },
                success: function(data) {
                    $('.canvas-builder').html(data.template);
                }
            });
        },
    });
});