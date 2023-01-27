const tooltipTriggerList = [].slice.call(document.querySelectorAll('#tooltip'));
const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
});

function send_fail_body(message) {
    const body = $(".send-fail-body");
    body.empty()
    body.append(message)
    new bootstrap.Toast(document.querySelector('.send-fail')).show()
}

function send_success_body(message) {
    const body = $(".send-success-body");
    body.empty()
    body.append(message)
    new bootstrap.Toast(document.querySelector('.send-success')).show()
}

$('#get-email-code').click(function () {
    let time = 120;
    console.log("click!")
    const email_code = $('#get-email-code');
    email_code.attr("disabled", "")
    const pattern = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
    const email = $("#email").val()
    if (!pattern.test(email)) {
        send_success_body("请输入正确的邮箱!")
        return
    }
    $.ajax({
        type: "POST",
        url: "/api/v1/user/login/email/send_code",
        data: {"email": email},
        dataType: "json",
        success: function (message) {
            if (message['code'] === 0) {
                send_success_body("发送认证码成功!")
                localStorage.setItem("captcha_key", message['data']['captcha_key'])
                return
            }
            send_fail_body("发送认证码失败!" + message['msg'])
        },
        error: function (message) {
            send_fail_body("发送认证码失败! " + message)
        }
    })
    const interval = setInterval(function () {
        if (time === 0) {
            email_code.removeAttr("disabled")
            email_code.attr("value", "获取认证码")
            console.log("cleared")
            clearInterval(interval)
            return
        }
        email_code.attr("value", time + "秒后再试")
        time = time - 1
    }, 1000)
})

$('#login').click(function () {
    const email_code = $("#email-code").val()
    const email = $("#email").val()
    const captcha_key = localStorage.getItem("captcha_key")
    const pattern = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
    if (isNaN(Number(email_code))) {
        send_success_body("请输入正确的邮箱认证码!")
        return
    }
    if (!captcha_key) {
        send_success_body("请先获取邮箱认证码!")
        return
    }
    if (!pattern.test(email)) {
        send_success_body("请输入正确的邮箱!")
        return
    }
    $.ajax({
        type: "POST",
        url: "/api/v1/user/login/email",
        data: {"email": email, "captcha_key": captcha_key, "code": email_code},
        dataType: "json",
        success: function (message) {
            console.log(message)
            if (message['code'] === 0) {
                send_success_body("登录成功!")
                localStorage.removeItem("captcha_key")
                setTimeout(function () {
                    location.reload()
                }, 1500)
                return
            }
            if (message['code'] === 10004) {
                send_fail_body(message['msg'])
                return
            }
            send_fail_body("登录失败! " + message['msg'])
        },
    })
})

$("#logout").click(function () {
    $.ajax({
        type: "POST",
        url: "/api/v1/user/logout",
        dataType: "json",
        success: function (message) {
            console.log(message)
            if (message['code'] === 0) {
                location.reload()
            }
        }
    })
})