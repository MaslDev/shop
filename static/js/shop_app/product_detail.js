$.validator.addMethod("phoneValidation", function (value, element) {
    return this.optional(element) || /^\+?1?\d{9,15}$/i.test(value);
}, "Phone invalid format");

$(document).ready(function () {
    $('#product-detail-title-image').imageLens({borderSize: 1, lensSize: 150}); // plagin init
    $('.other-image img').click(function () {
        let $thisSrc = this.src;
        let titleImage = $('#product-detail-title-image');
        titleImage.attr('src', $thisSrc);
        titleImage.imageLens({borderSize: 1, lensSize: 150});
    });
});





