const box = $(".preview-box")
const round = $(".preview-box-round")
box.hide()
round.hide()
let CROPPER = null;
const file_type = ['.jpg', '.png', '.jpeg']

function edit_fail_information(message) {
    const body = $(".edit-fail-body");
    body.empty()
    body.append(message)
    new bootstrap.Toast(document.querySelector('.edit-fail')).show()
}

function get_extension(name) {
    return name.substring(name.lastIndexOf("."))
}

function update_file() {
    document.querySelector('#img-reader').click()
    if (CROPPER) {
        CROPPER.destroy()
    }
}

function loadingImg() {

    //读取上传文件
    let reader = new FileReader();
    if (event.target.files[0]) {

        //readAsDataURL方法可以将File对象转化为data:URL格式的字符串（base64编码）
        reader.readAsDataURL(event.target.files[0]);
        if (!file_type.includes(get_extension(event.target.files[0].name).toLowerCase())) {
            alert("文件格式错误!")
            $('#img-reader').val("")
            return
        }
        box.show()
        round.show()
        reader.onload = () => {
            //将img的src改为刚上传的文件的转换格式
            document.querySelector('#crop-img').src = reader.result;
            $('#crop-img').on("error", function () {
                alert("图片加载失败")
                $('#img-reader').val("")
                document.querySelector('#crop-img').src = "https://laosun-video.obs.cn-north-4.myhuaweicloud.com/avatar/empty.png"
                box.hide()
                round.hide()
            })
            const image = document.getElementById('crop-img');

            //创建cropper实例-----------------------------------------
            CROPPER = new Cropper(image, {
                aspectRatio: 1,
                viewMode: 1,
                background: false,
                zoomable: false,
                guides: false,
                minContainerWidth: 512,
                minContainerHeight: 512,
                dragMode: 'move',
                preview: [document.querySelector('.preview-box'),
                    document.querySelector('.preview-box-round')]
            })
        }
    }
}

function update_avatar() {
    const files = $('#img-reader')[0].files
    // 2. 判断是否选择了文件
    if (files.length <= 0) {
        alert('请选择图片后再上传！')
        return
    }
    CROPPER.getCroppedCanvas({
        maxWidth: 512,
        maxHeight: 512,
        fillColor: '#fff',
        imageSmoothingEnabled: true,
        imageSmoothingQuality: 'high',
    }).toBlob((blob) => {
        const formData = new FormData();
        formData.append('avatar', blob);
        $.ajax({
            url: "/api/v1/user/account/edit_avatar",
            type: "POST",
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
                if (data['code'] === 0) {
                    new bootstrap.Toast(document.querySelector('.edit-success')).show()
                    setTimeout(function () {
                        location.reload()
                    }, 1500)
                } else {
                    edit_fail_information(data['msg'])
                }
            }
        });
    })
}
