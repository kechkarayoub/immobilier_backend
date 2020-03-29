(function($) {
    setTimeout(function(){
        var $ = $ || django.jQuery;
        $("#contactbuy_form .submit-row .default").val("Return");
        $("#contactbuy_form .submit-row input[name=_continue]").addClass("hidden");
        $("#contactbuy_form .submit-row .deletelink-box").addClass("hidden");
        $("#contactbuy_form").find("input, textarea").attr("readonly", true);
    }, 500);
})(django.jQuery);