$(function () {
    // ajax：登录表单
    $('#submit-login').click(function () {
        $.ajax({
            url: '/login/',
            type: 'post',
            data: {
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
                'username_login': $('#id_username_login').val(),
                'password_login': $('#id_password_login').val(),
                'verify_code_str_login': $('#verify-code-str-login').val(),
            },
            success: function (data) {
                if (data.user) {
                    window.location.reload()
                } else {
                    // 清除所有错误信息
                    $('span.error').html('');
                    // 展示最新错误信息
                    $.each(data.msg, function (name, error_list) {
                        if (name == 'verify-code-str-login') {
                            $('#verify-code-str-login').next().html(error_list[0]);
                        } else if (name == 'user-pwd-login') {
                            $('#id_password_login').next().html(error_list[0]);
                        } else {
                            $('#id_' + name).next().html(error_list[0]);
                        }
                    });
                }
            }
        })
    })

    // ajax：注册表单
    $('#submit-reg').click(function () {
        let form_data = new FormData();
        let request_data = $('#form_reg').serializeArray();
        // 打包form表单数据
        $.each(request_data, function (index, data) {
            form_data.append(data.name, data.value)
        })
        form_data.append('verify_code_str_reg', $('#verify-code-str-reg').val());
        form_data.append('avatar_reg', $('#id_avatar_reg')[0].files[0]);
        $.ajax({
            url: '/reg/',
            type: 'post',
            contentType: false,
            processData: false,
            data: form_data,
            success: function (data) {
                if (data.user) {
                    location.href = '/home/';
                } else {
                    // 清除所有错误信息
                    $('span.error').html('');
                    // 展示最新错误信息
                    $.each(data.msg, function (name, error_list) {
                        if (name == '__all__') {
                            $('#id_r_password_reg').next().html(error_list[0]);
                        } else if (name == 'verify-code-str-reg') {
                            $('#verify-code-str-reg').next().html(error_list[0]);
                        } else {
                            $('#id_' + name).next().html(error_list[0]);
                        }
                    })
                }
            }
        })
    })

    // ajax：修改站点标题
    $('#submit-change-site-title').click(function () {
        $.ajax({
            url: '/change_site_title/',
            type: 'post',
            data: {
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
                'site_title': $('#id_site_title').val(),
                'site_id': $('#id_site_title').attr('site_id'),
            },
            success: function (data) {
                window.location.reload()
            }
        })
    })

    // 手动点击刷新验证码
    $('.verify-code-img').click(function () {
        $(this)[0].src += '?';
    })

    // 自动刷新验证码
    $('.auth').click(function () {
        $('.verify-code-img')[0].src += '?';
        $('.verify-code-img')[1].src += '?';
    })

    // 注册时刷新头像
    $('#id_avatar_reg').change(function () {
        // 获取选取的文件对象
        let file_obj = $('#id_avatar_reg')[0].files[0];
        // 获取文件路径
        let reader = new FileReader();
        reader.readAsDataURL(file_obj);
        // 修改img标签src路径
        reader.onload = function () {
            $('.avatar-reg img').attr('src', reader.result)
        }
    })

    // 标签页toggle
    $('#myTabs a').click(function (e) {
        e.preventDefault()
        $(this).tab('show')
    })

    // 欢迎页
    $('#welcome-btn').click(function () {
        $('.welcome').stop().fadeOut(300)
    })
    setTimeout(function () {
        $('.welcome').stop().slideDown(600)
    }, 1000)


    // 给文章卡片增加超链接
    $('.article-item').click(function () {
        let a_href = $($(this).find('a').get(0)).attr('href')
        location.href = a_href;
    })
})
