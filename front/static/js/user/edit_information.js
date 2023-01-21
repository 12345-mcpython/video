function edit_fail_information(message) {
    const body = $(".edit-fail-body");
    body.empty()
    body.append(message)
    new bootstrap.Toast(document.querySelector('.edit-fail')).show()
}

$("#information-save").click(function () {
    console.log("clicked")
    const username = $("#username").val()
    const description = $("#description").val()
    if (username.length >= 16) {
        edit_fail_information("用户名长度不得超过16个字符!")
        return
    }
    if (description.length >= 500) {
        edit_fail_information("个人签名长度不得超过128个字符!")
        return
    }
    $.ajax({
        type: "POST",
        url: "/api/v1/user/account/edit_information",
        data: {"description": description, "username": username},
        dataType: "json",
        success: function (message) {
            if (message['code'] === 0) {
                new bootstrap.Toast(document.querySelector('.edit-success')).show()
                setTimeout(function () {
                    location.reload()
                }, 1500)
                return
            }
            edit_fail_information("修改失败! " + message['msg'])
        },
        error: function (message) {
            send_fail_body("修改失败! " + message)
        }
    })
})