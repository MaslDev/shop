$.validator.addMethod("passwordValidation", function (value, element) {
    return this.optional(element) || /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/i.test(value);
}, "Password invalid format");


$(document).ready(function () {
    $("#new-user-password-form").validate({
        rules: {
            current_password: {
                required: true,
                minlength: 8,
                passwordValidation: true
            },
            new_password: {
                required: true,
                minlength: 8,
                passwordValidation: true
            },
            new_password_confirm: {
                required: true,
                equalTo: "#new_password",
                minlength: 8,
                passwordValidation: true
            },
        },
        messages: {
            current_password: {
                required: "Please enter a password",
                minlength: "Your password must be at least 8 characters long"
            },
            new_password: {
                required: "Please enter a password",
                minlength: "Your password must be at least 8 characters long"
            },
            new_password_confirm: {
                required: "Please repeat the password",
                equalTo: "This password doesn't match with the original password",
                minlength: "Your password must be at least 8 characters long"
            },
        },
        submitHandler: function () {
            let $thisForm = $('#new-user-password-form');
            let $thisUrl = $thisForm.attr('data-url') || window.location.href;
            let $formData = $thisForm.serialize();
            $.ajax({
                method: 'POST',
                url: $thisUrl,
                data: $formData,
                success: function (response_data) {
                    if (response_data.response == 'current_pass_inc') {
                        alert("You entered an incorrect current password")
                    } else {
                        alert("'Your password has been successfully changed.");
                         window.location = '/';
                    }
                }

            });
        }

    });
});