// Flatpickr
var f1 = flatpickr($('.basicFlatpickr'));
var f2 = flatpickr($('.expiredDateTimeFlatpickr'), {
    enableTime: true,
    dateFormat: "Y-m-d H:i",
    time_24hr: true,
});
var f3 = flatpickr($('.rangeCalendarFlatpickr'), {
    mode: "range",
});
var f4 = flatpickr($('.timeFlatpickr'), {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    defaultDate: "13:45"
});
$("#clear-date").click(function() {
    $('.expiredDateTimeFlatpickr.expired').flatpickr().clear();
})