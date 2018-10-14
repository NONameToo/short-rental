function logout() {
    $.get("/api/logout", function(data){
        if (0 == data.errno) {
            location.href = "/";
        }
    })
}

$(document).ready(function(){
    $.get("/api/profile", function(data) {
        // alert(data.errno);
        // alert(data.errmsg);
        // alert(data.data['name']);
        // alert(data.data['mobile']);
        if ("4101" == data.errno) {
            window.location.href = "/login.html";
        }
        else if ("0" == data.errno) {
            $("#user-name").html(data.data.name);
            $("#user-mobile").html(data.data.mobile);
            if (data.data.avatar) {
                $("#user-avatar").attr("src", data.data.avatar);
            }
        }
    }, "json");
});