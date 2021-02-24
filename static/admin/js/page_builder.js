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

    $('.canvas-builder').on('click', '.col-canvas-replace', function (e) {
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

    function getAjaxForm(block) {
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

    function getCol6HTML() {
        return '<p class="d-block col-md-12 shadow-lg text-center py-4 round h1">6 - 6</p>';
    }

    function getCol3HTML() {
        return '<p class="d-block col-md-12 shadow-lg h3 text-center py-4 round">3 - 3 - 3 - 3</p>';
    }

    function getCol4HTML() {
        return '<p class="d-block col-md-12 shadow-lg h1 text-center py-4 round">4 - 4 - 4</p>';
    }

    function getCol84HTML() {
        return '<p class="d-block col-md-12 shadow-lg h1 text-center py-4 round">8 - 4</p>';
    }

    function getCol48HTML() {
        return '<p class="d-block col-md-12 shadow-lg h1 text-center py-4 rounded">4 - 8</p>';
    }

    function query_canvas_rows() {
        let canvasRows = $('.canvas-builder').children();
        for (var i = 0; i < canvasRows.length; i++) {
            if ($(canvasRows[i]).hasClass('empty')) {
                return canvasRows[i];
            }
        }
    }

    $(".row-canvas-droppable-6").draggable({
        cursor: 'move',
        revert:false,
        helper: function () {
            return getCol6HTML()
        },
        snapTo: '.empty',
        delay: 100,
        scrollSensitivity: 100,
        scrollSpeed: 20,
        opacity: 1,
        zIndex: 100,
        stop: function (ev, ui) {
            var row = query_canvas_rows();
            var canvas = $('.canvas-builder').data('id');
            var csrf = $('.canvas-builder').data('csrf');
            if (row && canvas)  {
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
                    success: function (data) {
                        $('.canvas-builder').html(data.template);
                    }
                });
            }
        },
    });
    $(".row-canvas-droppable-4").draggable({
        cursor: 'move',
        revert:false,
        helper: function () {
            return getCol4HTML()
        },
        snapTo: '.empty',
        delay: 100,
        scrollSensitivity: 100,
        scrollSpeed: 20,
        opacity: 1,
        zIndex: 100,
        stop: function (ev, ui) {
            var row = query_canvas_rows();
            var canvas = $('.canvas-builder').data('id');
            var csrf = $('.canvas-builder').data('csrf');

            if (row && canvas) {
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
                    success: function (data) {
                        $('.canvas-builder').html(data.template);
                    }
                });
            }
        },

    });
    $(".row-canvas-droppable-3").draggable({
        cursor: 'move',
        revert:false,
        helper: function () {
            return getCol3HTML()
        },
        snapTo: '.empty',
        delay: 100,
        scrollSensitivity: 100,
        scrollSpeed: 20,
        opacity: 1,
        zIndex: 100,
        stop: function (ev, ui) {
            var row = query_canvas_rows();
            var canvas = $('.canvas-builder').data('id');
            var csrf = $('.canvas-builder').data('csrf');
            if (row && canvas) {
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
                    success: function (data) {
                        $('.canvas-builder').html(data.template);
                    }
                });
            }
        },

    });
    $(".row-canvas-droppable-84").draggable({
        cursor: 'move',
        revert:false,
        helper: function () {
            return getCol84HTML()
        },
        snapTo: '.empty',
        delay: 100,
        scrollSensitivity: 100,
        scrollSpeed: 20,
        opacity: 1,
        zIndex: 100,
        stop: function (ev, ui) {
            var row = query_canvas_rows();
            var canvas = $('.canvas-builder').data('id');
            var csrf = $('.canvas-builder').data('csrf');
            if (row && canvas) {
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
                    success: function (data) {
                        $('.canvas-builder').html(data.template);
                    }
                });
            }
        },
    });
    $(".row-canvas-droppable-48").draggable({
        cursor: 'move',
        revert:false,
        helper: function () {
            return getCol48HTML()
        },
        snapTo: '.empty',
        delay: 100,
        scrollSensitivity: 100,
        scrollSpeed: 20,
        opacity: 1,
        zIndex: 100,
        stop: function (ev, ui) {
            var row = query_canvas_rows();
            var canvas = $('.canvas-builder').data('id');
            var csrf = $('.canvas-builder').data('csrf');
            if (row && canvas) {
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
                    success: function (data) {
                        $('.canvas-builder').html(data.template);
                    }
                });
            }
        },
    });
    $(".row-canvas-draggable").draggable({
        connectToSortable: ".canvas-builder",
        helper: function () {
            return getCanvasRowHTML();
        },
        revert: false,
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
                success: function (data) {
                    $('.canvas-builder').html(data.template);
                }
            });
        },

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