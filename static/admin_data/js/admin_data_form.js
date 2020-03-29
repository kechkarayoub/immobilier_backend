(function($) {
    setTimeout(function(){
        var $ = $ || django.jQuery;
        $(".field-image").on('change', 'input[type=file]', function(event){
            var self = this;
            var files = event.target.files;
            for (var i = 0, f; f = files[i]; i++){
                if (!f.type.match('image.*')){
                    continue;
                }
                var reader = new FileReader();
                reader.onload = (function(){
                    return function(e){
                        var img = $(self).closest(".module").find('.field-get_admin_image_preview img');
                        if(img.length){
                            $(img).attr("src", e.target.result);
                        }
                        else{
                            $(self).closest(".module").find(".field-get_admin_image_preview .readonly").html(
                                "<img src='" + e.target.result + "' width='150' height='150' style='object-fit: cover;'/>"
                            );
                        }

                    };
                })(f);
                reader.readAsDataURL(f);
            }
        });
        $("#id_enable_map").on('change', function(event){
            var self = this;
            if($(this).is(":checked")){
                $(this).closest(".module").find(".field-gps_latitude, .field-gps_longitude").removeClass("hidden");
            }
            else{
                $(this).closest(".module").find(".field-gps_latitude, .field-gps_longitude").addClass("hidden");
            }
        });
        if(!$("#id_enable_map").is(":checked")){
            $("#id_enable_map").closest(".module").find(".field-gps_latitude, .field-gps_longitude").addClass("hidden");
        }
        $("#admindata_form .submit-row input[name='_addanother']").addClass("hidden");
    }, 500);
})(django.jQuery);