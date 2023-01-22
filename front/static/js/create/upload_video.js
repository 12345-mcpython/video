function choose_video() {
    $("#choose-video").click()
}

const file_type = ['.jpg', '.png', '.jpeg']

let dplayer = null

let played = false

function get_extension(name) {
    return name.substring(name.lastIndexOf("."))
}

//获取uuid文件名称（去掉扩展名）
function get_filename(data) {
    return data.substring(0, data.indexOf("."));
}


function get_video() {
    $("#video-info").show()
    $("#play-video-button").show()
    const video_shower = $("#video-shower")
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
    $("#cover").click()
}

function loading_cover() {
    let reader = new FileReader();
    if (event.target.files[0]) {
        reader.readAsDataURL(event.target.files[0]);
        if (!file_type.includes(get_extension(event.target.files[0].name).toLowerCase())) {
            alert("文件格式错误!")
            $('#cover').val("")
            return
        }
        reader.onload = () => {
            document.querySelector('#img-cover').src = reader.result;
            $('#img-cover').on("error", function () {
                alert("图片加载失败")
                $('#cover').val("")
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

function publish_video(){

}