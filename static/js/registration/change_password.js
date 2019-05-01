$.validator.addMethod("passwordValidation", function (value, element) {
    return this.optional(element) || /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/i.test(value);
}, "Password invalid format");

$(document).ready(function () {
    $("#change-password-form").validate({
        rules: {
            password: {
                required: true,
                minlength: 8,
                passwordValidation: true
            },
            confirm_password: {
                required: true,
                equalTo: "#ChangePasswordFormPassword",
                minlength: 8,
                passwordValidation: true
            }
        },
        messages: {
            password: {
                required: "Please enter a password",
                minlength: "Your password must be at least 8 characters long"
            },
            confirm_password: {
                required: "Please repeat the password",
                equalTo: "This password doesn't match with the original password",
                minlength: "Your password must be at least 8 characters long"
            }
        },
        submitHandler: function () {
            var $thisForm = $('#change-password-form');
            var $password = $('#ChangePasswordFormPassword').val();
            var $thisUrl = $thisForm.attr('data-url') + '&password=' + $password || window.location.href;
            $.ajax({
                method: 'get',
                url: $thisUrl,
                dataType: 'json',
                success: function (response_data) {
                    if(response_data.response == 'success'){
                        alert('Your password has been successfully changed.');
                        window.location = '/';
                    }
                }

            });
        }

    });
});