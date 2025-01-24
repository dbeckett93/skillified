document.addEventListener("DOMContentLoaded", function() {
    function initializeDateTimePicker() {
        flatpickr(".datetimepicker", {
            enableTime: true,
            dateFormat: "Y-m-d H:i",
        });
    }

    function initializeDatePicker() {
        flatpickr(".datepicker", {
            dateFormat: "Y-m-d",
        });
    }

    // Call the functions to initialize the date time picker and date picker
    initializeDateTimePicker();
    initializeDatePicker();
});