$(document).ready(function () {
    $("#add-to-cart-form").validate({
        rules: {
            phone: {
                required: true,
                phoneValidation: true
            },
            quantity:{
                required:true,
            }
        },
        submitHandler: function () {
            let $thisForm = $('#add-to-cart-form');
            let $thisUrl = $thisForm.attr('data-url') || window.location.href;
            console.log($thisUrl)
            let $formData = $thisForm.serialize();
            $.ajax({
                method: 'POST',
                url: $thisUrl,
                data: $formData,
                success: function (response_data) {
                   if (response_data.response == 'success') {
                        alert("Product successfully added to cart.");
                   }
                }

            });
        }
    })
});