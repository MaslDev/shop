$('#sign-in').click(function () {
    $('#sign-in-modal').modal();
    var $remember = $.cookie('remember');
    if ($remember == 'true') {
        var $email = $.cookie('email');
        var $password = $.cookie('password');
        $('#LoginFormEmail').val($email);
        $('#LoginFormEmailLabel').addClass('active');
        $('#LoginFormPassword').val($password);
        $('#LoginFormPasswordLabel').addClass('active');
        $('#remember').prop('checked', $remember)
    }
});

$(document).ready(function () {
    var $sign_in_form = $('#sign-in-form');
    $sign_in_form.submit(function (event) {
        var $thisUrl = $sign_in_form.attr('data-url') || window.location.href;
        var $formData = $sign_in_form.serialize();
        event.preventDefault();
        $.ajax({
            method: 'POST',
            url: $thisUrl,
            data: $formData,
            success: function (response_data) {
                if (response_data.response == 'dismatch') {
                    alert("Your username and password didn't match. Please try again.")
                } else if (response_data.response == 'nouser') {
                    alert("We didn't find you! Please Register")
                } else {
                    window.location = '/'
                }
                if ($('#remember').is(':checked')) {
                    var $email = $('#LoginFormEmail').val();
                    var $password = $('#LoginFormPassword').val();
                    $.cookie('email', $email, {expires: 14});
                    $.cookie('password', $password, {expires: 14});
                    $.cookie('remember', true, {expires: 14});
                } else {
                    $.cookie('email', null);
                    $.cookie('password', null);
                    $.cookie('remember', null);
                }
            }
        });
    });
});