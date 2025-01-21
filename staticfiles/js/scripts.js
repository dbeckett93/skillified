document.addEventListener("DOMContentLoaded", function() {
    function initializeDateTimePicker() {
        flatpickr(".datetimepicker", {
            enableTime: true,
            dateFormat: "Y-m-d H:i",
        });
    }

    // Call the function to initialize the date time picker
    initializeDateTimePicker();
});
