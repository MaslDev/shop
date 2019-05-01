$.validator.addMethod("lettersonly", function (value, element) {
    return this.optional(element) || /^[A-Za-zА-Яа-яЁё]+$/i.test(value);
}, "Letters only please");

$.validator.addMethod("passwordValidation", function (value, element) {
    return this.optional(element) || /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/i.test(value);
}, "Password invalid format");

$.validator.addMethod("phoneValidation", function (value, element) {
    return this.optional(element) || /^\+?1?\d{9,15}$/i.test(value);
}, "Phone invalid format");

$.validator.addMethod("emailValidation", function (value, element) {
    return this.optional(element) || /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i.test(value);
}, "Please enter a valid email address.");

$(document).ready(function () {
    $("#sign-up-form").validate({
        rules: {
            password: {
                required: true,
                minlength: 8,
                passwordValidation: true
            },
            confirm_password: {
                required: true,
                equalTo: "#RegisterFormPassword",
                minlength: 8,
                passwordValidation: true
            },
            email: {
                required: true,
                emailValidation: true
            },
            first_name: {
                required: true,
                lettersonly: true
            },
            last_name: {
                required: true,
                lettersonly: true

            },
            phone: {
                required: true,
                phoneValidation: true
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
            },
            email: {
                required: "Please enter a email"
            },
            phone: {
                required: "Please enter a phone"
            },
            first_name: {
                required: "Please enter a name"

            },
            last_name: {
                required: "Please enter a surname"

            }
        },
        submitHandler: function () {
            let $thisForm = $('#sign-up-form');
            let $thisUrl = $thisForm.attr('data-url') || window.location.href;
            var $formData = $thisForm.serialize();
            $.ajax({
                method: 'POST',
                url: $thisUrl,
                data: $formData,
                success: function (response_data) {
                    if (response_data.response == 'yesemail') {
                        alert("This email address already registered")
                    } else if (response_data.response == 'yesphone') {
                        alert("This phone address already registered")
                    } else {
                        alert("You need activate your account. We send message to your email. Thanks for registration");
                        $thisForm[0].reset();
                    }
                }

            });
        }

    });
});