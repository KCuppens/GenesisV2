$(document).ready(function () {
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
            success: function (data) {
                $('.canvas-builder').html(data.template);
            }
        });
    }

    $('.canvas-builder').on('click', '.row-canvas-delete', function (e) {
        e.stopPropagation();
        var canvas = $('.canvas-builder').data('id');
        var row = $('.row-canvas-delete').data('id');
        var csrf = $('.canvas-builder').data('csrf');
        $.ajax({
            type: 'POST',
            url: 'canvas-row',
            data: {
                'canvas': canvas,
                'action': 'delete',
                'row': row,
                'csrfmiddlewaretoken': csrf,
            },
            success: function (data) {
                $('.canvas-builder').html(data.template);
            }
        });
    });
    $('.canvas-builder').on('click', '.add-block', function (e) {
        e.stopPropagation();
        if ($(this).parent().hasClass('is-selected')) {
            $(this).parent().siblings().removeClass('is-selected');
            $(this).parent().removeClass('is-selected');
        } else {
            $(this).parent().siblings().removeClass('is-selected');
            $(this).parent().addClass('is-selected');
        }
        var row = $(this).data('row');
        var csrf = $('.canvas-builder').data('csrf');
        var canvas = $('.canvas-builder').data('id');
        console.log(row);
        $.ajax({
            type: 'POST',
            url: 'canvas-row',
            data: {
                'csrfmiddlewaretoken': csrf,
                'row': row,
                'canvas': canvas,
                'action': 'openmodal'
            },
            success: function (data) {
                $('.overview-blocks').html(data.template);
                $('#exampleModal').modal();
            }
        });
    });

    $('.canvas-builder').on('click', '.col-canvas-replace', function (e) {
        var row = $(this).data('row');
        var csrf = $('.canvas-builder').data('csrf');
        var canvas = $('.canvas-builder').data('id');
        $.ajax({
            type: 'POST',
            url: 'canvas-row',
            data: {
                'csrfmiddlewaretoken': csrf,
                'row': row,
                'canvas': canvas,
                'action': 'openmodal'
            },
            success: function (data) {
                $('.overview-blocks').html(data.template);
                $('#exampleModal').modal();
            }
        });
    });

    function getAjaxForm(block) {
        var csrf = $('.canvas-builder').data('csrf');
        var page = $('.canvas-builder').data('page');
        $.ajax({
            type: 'POST',
            url: 'canvas-content',
            data: {
                'csrfmiddlewaretoken': csrf,
                'block': block,
                'ajax': 'get',
                'page': page
            },
            success: function (data) {
                $('.block-content').html(data.template);       
            }
        });
    };

    $('.canvas-builder').on('click', '.col-canvas-edit', function (e) {
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
        return '<p class="d-block col-md-12 shadow-lg h1 text-center py-4 rounded">Add Row</p>';
    }

    function query_canvas_rows() {
        let canvasRows = $('.canvas-builder').children();
        for (var i = 0; i < canvasRows.length; i++) {
            if ($(canvasRows[i]).hasClass('empty')) {
                return canvasRows[i];
            }
        }
    }
    $(".row-canvas-draggable").on('click', function(){
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
            success: function (data) {
                $('.canvas-builder').html(data.template);
            }
        });
    });
    $('.canvas-builder').sortable({ 
        axis: 'y',
        placeholder: 'py-5',
        scrollSpeed: 20,
        revert: 'invalid',
        scrollSensitivity: 20,
        scroll: true,
    });
});