var curr_index = 1;
var donotload = false;

function parseHTML(data) {
    let str = ``;
    data.forEach(ele => {
        switch (ele.type) {
            case "paragraph":
                str += `<p>${ele.data.text}</p>`;
                break;
            case "Image":
                str += `<div class="post-img-wrapper">
                            <img src="${ele.data.file.url}">
                            <span>${ele.data.caption}</span>
                        </div>`;
                break;
            case "Attaches":
                let size=ele.data.file.size/1024;
                let unit='KB';
                if(size>1023){
                    size/=1024;
                    unit='MB';
                }
                size=Math.round(size * 100) / 100;
                str += `<div class="post-attaches-wrapper">		
                            <img src="/static/${ele.data.file.extension}-icon.svg">
                            <div>
                                <p>${ele.data.title}</p>
                                <p>${size} ${unit}</p>
                            </div>
                            <a href="${ele.data.file.url}">
                                <img src="/static/dl-icon.svg">
                            </a>
                        </div>`;
                break;

        }
    });
    return str;
}
var load_posts = function(index) {
    $.ajax({
        url: '/post/load-feed/' + index,
        dataType: 'json',
        success: function(data) {
            Array.prototype.forEach.call(data, (post) => {
                console.log(JSON.parse(post.content));
                var temp = document.getElementById("post-template");
                var p = temp.content.cloneNode(true);
                p.querySelector('.post-author').innerHTML = post.author;
                p.querySelector('.post-date').innerHTML = post.datetime;
                p.querySelector('.post-content').innerHTML = parseHTML(JSON.parse(post.content).blocks);
                p.querySelector('.post-like-count').innerHTML = post.like_count;
                if (post.is_liked) p.querySelector('.like-button img').setAttribute('src', '/static/like-liked.svg');
                else p.querySelector('.like-button img').setAttribute('src', '/static/like.svg');
                p.querySelector('.like-button').setAttribute('data-post-id', post.id);
                p.querySelector('.like-button img').setAttribute('id', 'like' + post.id.toString());
                p.querySelector('.post-like-count').setAttribute('id', 'likecount' + post.id.toString());
                document.getElementById('feed').appendChild(p);
                donotload = false;
            })
            initLikes();
        },
        error: function(data) {
            console.log(data.responseJSON.error);
        }
    })
}

$(document).ready(function() {
    load_posts(0);
});

function initLikes() {
    $('.like-button').on('click', function(e) {
        var id;
        id = $(this).attr("data-post-id");
        console.log(id);
        $.ajax({
            type: "GET",
            url: '/post/like-post',
            data: {
                post_id: id
            },
            success: function(data) {
                console.log(data);
                if (data == 'liked') {
                    $('#like' + id).attr('src', '/static/like-liked.svg');
                    var val = parseInt($('#likecount' + id).text());
                    $('#likecount' + id).text((val + 1).toString().replace(/^0+/, ''));
                } else if(data== 'unliked'){
                    $('#like' + id).attr('src', '/static/like.svg');
                    var val = parseInt($('#likecount' + id).text());
                    $('#likecount' + id).text((val - 1) ? (val - 1).toString().replace(/^0+/, '') : 0);
                } else{
                    console.log(data);
                }
            },
            error: function(data) {
                alert(data)
            }
        })
    });
}

$(window).scroll(function() {
    //console.log($(window).scrollTop(),$(document).height() , $(window).height())
    if ($(window).scrollTop() > $(document).height() - $(window).height() - 50 && !donotload) {
        load_posts(curr_index);
        curr_index += 1;
        donotload = true;
    }
});