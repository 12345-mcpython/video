function choose_video() {
    $("#choose-video").click()
}

const file_type = ['.jpg', '.png', '.jpeg']

let dplayer = null

let played = false

function publish_fail_information(message) {
    const body = $(".publish-fail-body");
    body.empty()
    body.append(message)
    new bootstrap.Toast(document.querySelector('.publish-fail')).show()
}

function get_extension(name) {
    return name.substring(name.lastIndexOf("."))
}


function get_filename(data) {
    return data.substring(0, data.indexOf("."));
}


function get_video() {
    $("#video-info").show()
    $("#play-video-button").show()
    const file = document.getElementById("choose-video").files[0]
    let binaryData = [];
    binaryData.push(file);
    const url = URL.createObjectURL(new Blob(binaryData))
    let type = "mp4";
    if (get_extension(file.name).toLowerCase() === ".flv") {
        type = "flv"
    }
    dplayer = new DPlayer({
        container: document.getElementById('dplayer'),
        video: {
            "url": url,
            "type": type
        }
    })
    const videoElement = $(".dplayer-video")[0]
    videoElement.addEventListener("canplay", function () {
        const width = videoElement.videoWidth;
        const height = videoElement.videoHeight;
        if (width / height !== 16 / 9) {
            console.log(width, height, width / height)
            alert("视频宽高错误!")
            location.reload()
        }
    })

    $("#video-title").val(get_filename(file.name))
}


function choose_cover() {
    $("#cover-file").click()
}

function loading_cover() {
    let reader = new FileReader();
    if (event.target.files[0]) {
        reader.readAsDataURL(event.target.files[0]);
        if (!file_type.includes(get_extension(event.target.files[0].name).toLowerCase())) {
            alert("文件格式错误!")
            $('#cover-file').val("")
            return
        }
        reader.onload = () => {
            document.querySelector('#img-cover').src = reader.result;
            $('#img-cover').on("error", function () {
                alert("图片加载失败")
                $('#cover-file').val("")
                document.querySelector('#img-cover').src = "https://laosun-video.obs.cn-north-4.myhuaweicloud.com/avatar/empty.png"
                $('#img-cover').hide()
            })
            const img = new Image()
            img.src = reader.result
            img.onload = function () {
                const width = img.width
                const height = img.height
                if (width / height !== 16 / 9) {
                    alert("图片宽高错误!")
                    document.querySelector('#img-cover').src = "https://laosun-video.obs.cn-north-4.myhuaweicloud.com/avatar/empty.png"
                    $('#img-cover').hide()
                }
            }
        }
        $('#img-cover').show()
    }
}

function generate_first_frame() {
    const videoElement = $(".dplayer-video")[0]
    const img_cover = $("#img-cover")
    videoElement.addEventListener("canplay", function () {
        let canvas = document.createElement("canvas");
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        canvas.getContext("2d").drawImage(videoElement, 0, 0, canvas.width, canvas.height);
        img_cover.attr("src", canvas.toDataURL("image/png"))
        img_cover.show()
    })
}


function data_to_blob(data_url) {
    let arr = data_url.split(','),
        mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]),
        n = bstr.length,
        u8arr = new Uint8Array(n)
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n)
    }
    return new Blob([u8arr], {type: mime})
}

function publish_video() {
    const title = $("#video-title").val()
    const description = $("#video-description").val()
    const tag = $("#video-tag").val()
    if (title === "" || description === "" || tag === "") {
        alert("请完善信息!")
    }
    const file = document.getElementById("choose-video").files[0]
    let video_content = [];
    video_content.push(file);
    const video_blob = new Blob(video_content)
    const cover_blob = data_to_blob($("#img-cover").attr("src"))
    const form_data = new FormData();
    form_data.append("files", video_blob)
    form_data.append("cover", cover_blob)
    form_data.append("title", title)
    form_data.append("description", description)
    form_data.append("tags", tag)
    $('.progress').show()
    $.ajax({
        url: "/api/v1/create/publish_video",
        type: "POST",
        data: form_data,
        contentType: false,
        processData: false,
        success: function (data) {
            if (data['code'] === 0) {
                new bootstrap.Toast(document.querySelector('.publish-success')).show()
                setTimeout(function () {
                    location.reload()
                }, 1500)
            } else {
                publish_fail_information(data['msg'])
            }
        },
        error: function (data) {
            console.log(data)
            publish_fail_information(data['responseText'])
        },
        xhr: function () {
            const xhr = $.ajaxSettings.xhr();
            if (xhr.upload) {
                xhr.upload.addEventListener('progress', function (e) {
                    let progress = (e.loaded / e.total) * 100
                    if (progress > 100) {
                        progress = 100
                    }
                    $('.progress-bar').css('width', progress + '%')
                })
                return xhr;
            }
        },
    })
}

function get_examine_speed(){
    $.ajax({
        url: "/api/v1/create/get_examine_speed",
        type: "GET",
        contentType: false,
        processData: false,
        success: function (data) {
            if (data['code'] === 0) {
                $(".examine-list").html("当前审核队列<span class='tag label label-info'>" + data['msg'] + "</span>, 总共审核队列数为" + data['data']['total'])
            } else {
                publish_fail_information(data['msg'])
            }
        },
        error: function (data) {
            console.log(data)
            publish_fail_information(data['responseText'])
        },
    })
}
$("html").ready(function (){
    get_examine_speed()
})