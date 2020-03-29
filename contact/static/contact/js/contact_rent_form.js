(function($) {
    setTimeout(function(){
        var $ = $ || django.jQuery;
        $("#contactbuy_form .submit-row input[name=_continue], #contactbuy_form .submit-row input[name=_addanother]").addClass("hidden");
        $("#contactbuy_form .submit-row .deletelink-box").addClass("hidden");
    }, 500);
})(django.jQuery);