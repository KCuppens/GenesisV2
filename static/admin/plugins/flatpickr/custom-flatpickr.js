// Flatpickr
var f1 = flatpickr($('.basicFlatpickr'));
var f2 = flatpickr($('.DateTimeFlatpickr'), {
    enableTime: true,
    dateFormat: "Y-m-d H:i:S",
    time_24hr: true,
    minDate: "today",
    defaultDate: "today"
});
var f2 = flatpickr($('.expiredDateTimeFlatpickr'), {
    enableTime: true,
    dateFormat: "Y-m-d H:i:S",
    time_24hr: true,
    minDate: "today",
});
var f3 = flatpickr($('.rangeCalendarFlatpickr'), {
    mode: "range",
});
var f4 = flatpickr($('.timeFlatpickr'), {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    time_24hr: true
});
$("#clear-date").click(function() {
    $('.expiredDateTimeFlatpickr.expired').flatpickr().clear();
})