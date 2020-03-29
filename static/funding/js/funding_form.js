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
                        var img = $(self).closest(".module").find('.field-get_user_image_preview img');
                        if(img.length){
                            $(img).attr("src", e.target.result);
                        }
                        else{
                            $(self).closest(".module").find(".field-get_user_image_preview .readonly").html(
                                "<img src='" + e.target.result + "' width='150' height='150' style='object-fit: cover;'/>"
                            );
                        }

                    };
                })(f);
                reader.readAsDataURL(f);
            }
        });
    }, 2000);
})(django.jQuery);