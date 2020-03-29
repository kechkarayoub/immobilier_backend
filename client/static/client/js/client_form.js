(function($) {
    function getCookie(cname) {
        var name = cname + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var ca = decodedCookie.split(';');
        for(var i = 0; i <ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }
//    $.ajaxSetup({
//        headers: {
//            'X-CSRF-Token': getCookie("csrftoken")
//        }
//    });
    setTimeout(function(){
        var $ = $ || django.jQuery;
        $('.btn-import').on('click', function(event){
            var self = this;
            $(this).closest("li").find("input.import_input").click();
        });
        $("li").on('change', 'input.import_input[type=file]', function(event){
            var self = this;
            var files = event.target.files;
            if(files.length == 0){
                return;
            }
            var formdata = new FormData();
            formdata.append("file", files[0]);
            $.ajax({
                url: "/en/api/client/import",
                type: "POST",
                method : "POST",
                enctype: 'multipart/form-data',
                data: formdata,
                processData: false,
                contentType: false,
                success: function (result) {
                    var message = result.message || "";
                    if(result.success){
                        if(result.clients_created){
                            message = message + "\r\n" + "Clients ajoutés: " + result.clients_created + ".";
                        }
                        if(result.clients_updated){
                            message = message + "\r\n" + "Clients modifiés: " + result.clients_updated + ".";
                        }
                        if(result.issues){
                            if(result.clients_created || result.clients_updated){
                                message = message + "\r\n" + "Les autres clients ne sont pas ajoutés en raison des problèmes suivants:";
                            }
                            else{
                                message = message + "\r\n" + "Les clients ne sont pas ajoutés en raison des problèmes suivants:";
                            }
                            Object.keys(result.issues).map(sheet_name => {
                                if(result.issues[sheet_name].length > 0){
                                    message = message + "\r\n" + "Dans la feille " + sheet_name + ":";
                                    result.issues[sheet_name].map(issue => {
                                        message = message + "\r\n    " + issue;
                                    });
                                }
                            });
                        }
                    }
                    alert(message);
                    if(result.success){
                        location.reload();
                    }
                },
                error: function(error) {
                        alert(error);
                }
            });
        });
    }, 500);
})(django.jQuery);