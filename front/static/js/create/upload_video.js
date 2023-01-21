function choose_video() {
    $("#choose-video").click()
}

const file_type = ['.jpg', '.png', '.jpeg']

function get_extension(name) {
    return name.substring(name.lastIndexOf("."))
}


function get_video() {
    $("#video-info").show()
    const video_shower = $("#video-shower")
    const file = document.getElementById("choose-video").files[0]
    let binaryData = [];
    binaryData.push(file);
    const url = URL.createObjectURL(new Blob(binaryData))
    video_shower.show()
    if (get_extension(file.name).toLowerCase() === ".flv") {
        if(!flvjs.isSupported()){
            alert("浏览器不支持flv.js, 请更换浏览器")
            return
        }
        const flvPlayer = flvjs.createPlayer({
            type: 'flv',
            url: url
        });
        flvPlayer.attachMediaElement(video_shower)
        flvPlayer.load()
        flvPlayer.play()
        return
    }
    video_shower.attr("src", url)
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

