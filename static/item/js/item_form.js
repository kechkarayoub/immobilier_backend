(function($) {
    setTimeout(function(){
        var $ = $ || django.jQuery;
        $("#images-group").on('change', '.field-image input[type=file]', function(event){
            var self = this;
            var files = event.target.files;
            for (var i = 0, f; f = files[i]; i++){
                if (!f.type.match('image.*')){
                    continue;
                }
                var reader = new FileReader();
                reader.onload = (function(){
                    return function(e){
                        var img = $(self).closest(".inline-related").find('.field-get_item_images_preview img');
                        if(img.length){
                            $(img).attr("src", e.target.result);
                        }
                        else{
                            $(self).closest(".module").find(".field-get_item_images_preview .readonly").html(
                                "<img src='" + e.target.result + "' width='150' height='150' style='object-fit: cover;'/>"
                            );
                        }

                    };
                })(f);
                reader.readAsDataURL(f);
            }
        });
        $(".field-image_map").on('change', 'input[type=file]', function(event){
            var self = this;
            var files = event.target.files;
            for (var i = 0, f; f = files[i]; i++){
                if (!f.type.match('image.*')){
                    continue;
                }
                var reader = new FileReader();
                reader.onload = (function(){
                    return function(e){
                        var img = $(self).closest(".inline-related").find('.field-get_item_image_map_preview img');
                        if(img.length){
                            $(img).attr("src", e.target.result);
                        }
                        else{
                            $(self).closest(".module").find(".field-get_item_image_map_preview .readonly").html(
                                "<img src='" + e.target.result + "' width='150' height='150' style='object-fit: cover;'/>"
                            );
                        }

                    };
                })(f);
                reader.readAsDataURL(f);
            }
        });
        $("#id_with_map").on('change', function(event){
            var self = this;
            if($(this).is(":checked")){
                $(this).closest(".module").find(".field-gps_latitude, .field-gps_longitude, .field-image_map.field-get_item_image_map_preview").removeClass("hidden");
            }
            else{
                $(this).closest(".module").find(".field-gps_latitude, .field-gps_longitude, .field-image_map.field-get_item_image_map_preview").addClass("hidden");
            }
        });
        if(!$("#id_with_map").is(":checked")){
            $("#id_with_map").closest(".module").find(".field-gps_latitude, .field-gps_longitude, .field-image_map.field-get_item_image_map_preview").addClass("hidden");
        }
    }, 500);
})(django.jQuery);