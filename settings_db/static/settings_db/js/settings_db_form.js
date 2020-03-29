(function($) {
    setTimeout(function(){
        var $ = $ || django.jQuery;
        $(".field-header_background_image").on('change', 'input[type=file]', function(event){
            var self = this;
            var files = event.target.files;
            for (var i = 0, f; f = files[i]; i++){
                if (!f.type.match('image.*')){
                    continue;
                }
                var reader = new FileReader();
                reader.onload = (function(){
                    return function(e){
                        var img = $(self).closest(".module").find('.field-get_header_background_image_preview img');
                        if(img.length){
                            $(img).attr("src", e.target.result);
                        }
                        else{
                            $(self).closest(".module").find(".field-get_header_background_image_preview .readonly").html(
                                "<img src='" + e.target.result + "' width='150' height='150' style='object-fit: cover;'/>"
                            );
                        }
                    };
                })(f);
                reader.readAsDataURL(f);
            }
        });
        $(".field-header_image").on('change', 'input[type=file]', function(event){
            var self = this;
            var files = event.target.files;
            for (var i = 0, f; f = files[i]; i++){
                if (!f.type.match('image.*')){
                    continue;
                }
                var reader = new FileReader();
                reader.onload = (function(){
                    return function(e){
                        var img = $(self).closest(".module").find('.field-get_header_image_preview img');
                        if(img.length){
                            $(img).attr("src", e.target.result);
                        }
                        else{
                            $(self).closest(".module").find(".field-get_header_image_preview .readonly").html(
                                "<img src='" + e.target.result + "' width='150' height='150' style='object-fit: cover;'/>"
                            );
                        }
                    };
                })(f);
                reader.readAsDataURL(f);
            }
        });
        $(".field-logo").on('change', 'input[type=file]', function(event){
            var self = this;
            var files = event.target.files;
            for (var i = 0, f; f = files[i]; i++){
                if (!f.type.match('image.*')){
                    continue;
                }
                var reader = new FileReader();
                reader.onload = (function(){
                    return function(e){
                        var img = $(self).closest(".module").find('.field-get_logo_image_preview img');
                        if(img.length){
                            $(img).attr("src", e.target.result);
                        }
                        else{
                            $(self).closest(".module").find(".field-get_logo_image_preview .readonly").html(
                                "<img src='" + e.target.result + "' width='150' height='150' style='object-fit: cover;'/>"
                            );
                        }
                    };
                })(f);
                reader.readAsDataURL(f);
            }
        });
        $(".field-main_bg_image").on('change', 'input[type=file]', function(event){
            var self = this;
            var files = event.target.files;
            for (var i = 0, f; f = files[i]; i++){
                if (!f.type.match('image.*')){
                    continue;
                }
                var reader = new FileReader();
                reader.onload = (function(){
                    return function(e){
                        var img = $(self).closest(".module").find('.field-get_main_bg_image_preview img');
                        if(img.length){
                            $(img).attr("src", e.target.result);
                        }
                        else{
                            $(self).closest(".module").find(".field-get_main_bg_image_preview .readonly").html(
                                "<img src='" + e.target.result + "' width='150' height='150' style='object-fit: cover;'/>"
                            );
                        }
                    };
                })(f);
                reader.readAsDataURL(f);
            }
        });
        $("#settingsdb_form .submit-row input[name='_addanother']").addClass("hidden");
    }, 500);
})(django.jQuery);