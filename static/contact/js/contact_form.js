(function($) {
    setTimeout(function(){
        var $ = $ || django.jQuery;
        $("#contact_form .submit-row .default").val("Return");
        $("#contact_form .submit-row input[name=_continue]").addClass("hidden");
        $("#contact_form .submit-row .deletelink-box").addClass("hidden");
        $("#contact_form").find("input, textarea").attr("readonly", true);
    }, 500);
})(django.jQuery);