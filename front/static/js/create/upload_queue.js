$("body").ready(
    $.ajax({
        url: "/api/v1/create/get_tasks",
        type: "GET",
        contentType: false,
        processData: false,
        success: function (data) {
            console.log(data['data'])
            let html = ""
            for (let i in data['data']) {
                i = data['data'][i]
                html += "<tr>"
                if (i['state'] === "FAILURE") {
                    html += "<td>" + "NO VIDEO" + "</td>"
                } else {
                    html += "<td>" + i['result']['video'] + "</td>"
                }
                if (i["state"] === "PROGRESS") {
                    html += "<td>" + "进行" + "</td>"
                    html += "<td>" + i['result']['progress'] + "%" + " </td>"
                }
                if (i["state"] === "SUCCESS") {
                    html += "<td>" + "完成" + "</td>"
                    html += "<td>" + "100%" + " </td>"
                }
                if (i['state'] === "FAILURE") {
                    html += "<td>" + "失败" + "</td>"
                    html += "<td>" + "0%" + " </td>"
                }

                html += "</tr>"
            }
            $("#queue-body").html(html)
        },
        error: function (data) {
            console.log(data)
        }
    })
)