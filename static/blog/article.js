let is_show = true;
$(function () {
    let comment_parent_id = '';
    let user_name_parent = '';
    // 点赞
    $('.article-like').click(function () {
        let is_like = $(this).hasClass('is-like');
        let article_like_count = $(this).children('.article-like-count')
        $.ajax({
            url: '/article_like/',
            type: 'post',
            data: {
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
                'is_like': is_like,
                'article_id': $('#article_title_id').attr('article_id'),
            },
            success: function (data) {
                if (data.is_success) {
                    let val = article_like_count.text();
                    article_like_count.text(parseInt(val) + 1);
                } else {
                    if (data.msg) {
                        $('.like-error').html(data.msg)
                    } else {
                        let val = data.is_like ? '您已喜欢过' : '您已踩过';
                        $('.like-error').html(val)
                    }
                    setTimeout(function () {
                        $('.like-error').html('')
                    }, 1000)
                }
            }
        })
    })
    // 展示评论
    if (is_show) {
        is_show = false
        $.ajax({
            url: '/article_comment_tree/',
            type: 'post',
            data: {
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
                'article_id': $('#article_title_id').attr('article_id'),
            },
            success: function (data) {
                let counter = 0;
                $.each(data, function (index, comment_obj) {
                    let pk = comment_obj.pk;
                    let content = comment_obj.content;
                    let comment_parent_id = comment_obj.comment_parent_id;
                    let user_name = comment_obj.user_name;
                    let create_time = comment_obj.create_time;
                    // 根评论
                    if (!comment_parent_id) {
                        let val = `
                                <li class="" comment_id="${pk}">
                                    <div>
                                        <a class="counter" href="">#${counter + 1}楼</a>
                                        <span class="text-muted small">${create_time}</span>
                                        <a href="/${user_name}/" class="small">${user_name}</a>
                                        <a class="pull-right replay small" href="javascript:0" comment_parent_id="${pk}" comment_user="${user_name}">回复</a>
                                    </div>
                                    <div>
                                        <p class="h5">${content}</p>
                                    </div>
                                </li>
                                <hr>
                            `;
                        counter += 1;
                        $('.comment-tree').append(val);
                    }
                    // 子评论
                    else {
                        let val = `
                                <li class="well" comment_id="${pk}">
                                    <div>
                                        <span class="text-muted small">${create_time}</span>
                                        <a href="/${user_name}/" class="small">${user_name}</a>
                                        <a class="pull-right replay small" href="javascript:0" comment_parent_id="${pk}" comment_user="${user_name}">回复</a>
                                    </div>
                                    <div>
                                        <p class="h5">${content}</p>
                                    </div>
                                </li>
                            `;
                        $(`[comment_id="${comment_parent_id}"]`).append(val);
                    }
                })

            }
        })
    }
    // 发布评论
    $('#submit-comment').click(function () {
        let content = $('#content').val();
        if (comment_parent_id) {
            let index = content.indexOf('\n');
            content = content.slice(index + 1)
        }
        console.log('当前评论内容：', content);
        $.ajax({
            url: '/article_comment/',
            type: 'post',
            data: {
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
                'content': content,
                'article_id': $('#article_title_id').attr('article_id'),
                'comment_parent_id': comment_parent_id,
            },
            success: function (data) {
                console.log('article_comment返回的数据：', data);
                // 评论成功：清空评论输入框
                $('#content').val('');
                // 评论成功：评论数+1
                let val = $('.article-comment-count').text();
                $('.article-comment-count').text(parseInt(val) + 1);
                // 评论成功：重置父评论id
                comment_parent_id = '';
                // 清空全部评论
                $('.comment-tree').html('');
                // 重新加载最新评论
                $.ajax({
                    url: '/article_comment_tree/',
                    type: 'post',
                    data: {
                        'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
                        'article_id': $('#article_title_id').attr('article_id'),
                    },
                    success: function (data) {
                        console.log(data)
                        let counter = 0;
                        $.each(data, function (index, comment_obj) {
                            let pk = comment_obj.pk;
                            let content = comment_obj.content;
                            let comment_parent_id = comment_obj.comment_parent_id;
                            let user_name = comment_obj.user_name;
                            let create_time = comment_obj.create_time;
                            // 根评论
                            if (!comment_parent_id) {
                                let val = `
                                            <li class="" comment_id="${pk}">
                                                <div>
                                                    <a class="counter" href="">#${counter + 1}楼</a>
                                                    <span class="text-muted small">${create_time}</span>
                                                    <a href="/${user_name}/" class="small">${user_name}</a>
                                                    <a class="pull-right replay small" href="javascript:0" comment_parent_id="${pk}" comment_user="${user_name}">回复</a>
                                                </div>
                                                <div>
                                                    <p class="h5">${content}</p>
                                                </div>
                                            </li>
                                            <hr>
                                        `;
                                counter += 1;
                                $('.comment-tree').append(val);
                            }
                            // 子评论
                            else {
                                let val = `
                                            <li class="well" comment_id="${pk}">
                                                <div>
                                                    <span class="text-muted small">${create_time}</span>
                                                    <a href="/${user_name}/" class="small">${user_name}</a>
                                                    <a class="pull-right replay small" href="javascript:0" comment_parent_id="${pk}" comment_user="${user_name}">回复</a>
                                                </div>
                                                <div>
                                                    <p class="h5">${content}</p>
                                                </div>
                                            </li>
                                        `;
                                $(`[comment_id="${comment_parent_id}"]`).append(val);
                            }
                        })

                    }
                })
            }
        });
    })
    // 发布子评论
    $('.comment-list').on('click', '.replay', function () {
        $('#content').focus();
        user_name_parent = $(this).attr('comment_user');
        let val = '回复' + user_name_parent + ':\n';
        $('#content').val(val);
        comment_parent_id = $(this).attr('comment_parent_id');
        console.log('父评论id：', comment_parent_id);
    })
})