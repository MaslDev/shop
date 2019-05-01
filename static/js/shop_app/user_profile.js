$.validator.addMethod("lettersonly", function (value, element) {
    return this.optional(element) || /^[A-Za-zА-Яа-яЁё]+$/i.test(value);
}, "Letters only please");

$.validator.addMethod("phoneValidation", function (value, element) {
    return this.optional(element) || /^\+?1?\d{9,15}$/i.test(value);
}, "Phone invalid format");

$(document).ready(function () {
    $("#user-profile-form").validate({
        rules: {
            first_name: {
                lettersonly: true
            },
            last_name: {
                lettersonly: true

            },
            phone: {
                phoneValidation: true
            }
        },
        submitHandler: function () {
            let $thisForm = $('#user-profile-form');
            let $thisUrl = $thisForm.attr('data-url') || window.location.href;
            let $formData = $thisForm.serialize();
            $.ajax({
                method: 'POST',
                url: $thisUrl,
                data: $formData,
                success: function (response_data) {
                   if (response_data.response == 'success') {
                        alert("Your data has been successfully saved.");
                   }
                }

            });
        }
    });
});