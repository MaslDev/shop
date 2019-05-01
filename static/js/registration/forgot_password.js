$.validator.addMethod("emailValidation", function (value, element) {
    return this.optional(element) || /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i.test(value);
}, "Please enter a valid email address.");

$(document).ready(function () {
    $("#forgot-password-form").validate({
        rules: {
            email: {
                required: true,
                emailValidation: true
            }
        },
        messages: {
            email: {
                required: "Please enter a email"
            }
        },
        submitHandler: function () {
            var $thisForm = $('#forgot-password-form');
            var $thisUrl = $thisForm.attr('data-url') || window.location.href;
            var $formData = $thisForm.serialize();
            $.ajax({
                method: 'POST',
                url: $thisUrl,
                data: $formData,
                success: function (response_data) {
                    if(response_data.response == 'success'){
                        alert("We sent you email instructions for changing your password")
                    } else if(response_data.response == 'nouser'){
                        alert("We didn't find you! Please Register")
                    }
                }

            });
        }
    });
});