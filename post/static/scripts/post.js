var curr_index = 1;
var donotload = false;
var firstload = true;
var username;
var csrf_token = ""

function parseHTML(data) {
    let str = ``;
    data.forEach(ele => {
        switch (ele.type) {
            case "paragraph":
                let fontSize = ele.data.text.length >= 120 ? 'sm':'lg';
                let px = ele.data.text.length >= 120 ? 'px-2' : 'px-4'
                str += `<p class="text-${fontSize} ${px} text-gray-500 mt-4 w-full text-justify">${ele.data.text}</p>`;
                break;
            case "Image":
                str += `<div class="post-img-wrapper mt-6 w-full">
                            <img src="${ele.data.file.url}" class="w-full">
                            <span class="text-sm text-gray-400 italic mt-2">${ele.data.caption}</span>
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
                str += `<div class="post-attaches-wrapper mt-6 h-15 w-4/5 p-3 bg-gray-100 rounded flex items-center justify-between">		
                            <div class="flex items-center">
                                <img class = "h-10 w-10" src="/static/img/${ele.data.file.extension}-icon.svg">
                                <div class = "ml-2">
                                    <p class = "text-md text-gray-500">${ele.data.title}</p>
                                    <p class = "text-sm text-gray-400">${size} ${unit}</p>
                                </div>
                            </div>
                            <a href="${ele.data.file.url}">
                                <img class = "h-10 w-10" src="/static/img/dl-icon.svg">
                            </a>
                        </div>`;
                break;
        }
    });
    return str;
}
var load_posts = function(index) {
    let tags = [];
    $('.feed-tag').each((ind,ele)=>{
        if(ele.textContent.length)
            tags.push(ele.textContent);
    });
    $.ajax({
        url: '/post/load-feed/' + index,
        dataType: 'json',
        type: 'POST',
        data: {'tags': JSON.stringify(tags), 'csrfmiddlewaretoken':csrf_token},
        success: function(data) {
            Array.prototype.forEach.call(data, (post) => {
                console.log(post);
                var temp = document.getElementById("post-template");
                var p = temp.content.cloneNode(true);
                p.id = 'post-' + post.id;
                p.querySelector('.post-author').setAttribute('href',`account/${post.author.username}`);
                p.querySelector('.post-author-name').innerHTML = post.author.name;
                p.querySelector('.post-author-img').setAttribute('src',post.author.profile_img)
                p.querySelector('.post-date').innerHTML = post.datetime;
                p.querySelector('.post-content').innerHTML = parseHTML(JSON.parse(post.content).blocks);
                p.querySelector('.like-count').innerHTML = post.like_count;
                p.querySelector('.comment-count').innerHTML = post.comment_count;
                if (post.is_liked) {
                    $(p.querySelector('.like-button svg')).addClass('svg-accent');
                    $(p.querySelector('.like-button p')).addClass('text-accent');
                }
                p.querySelector('.like-button').setAttribute('data-post-id', post.id);
                p.querySelector('.like-button svg').setAttribute('id', 'like' + post.id.toString());
                p.querySelector('.like-count').setAttribute('id', 'likecount' + post.id.toString());
                p.querySelector('.comment-count').setAttribute('id', 'commentcount' + post.id.toString());
                p.querySelector('.comment-button').addEventListener('click', function(){
                    showcomment(this);
                } );
                p.querySelector('.comment-button').setAttribute('data-post-id', post.id);
                document.getElementById('feed').appendChild(p);
                donotload = false;
                firstload=false;
                initLikes($(`.like-button[data-post-id=${post.id}]`)[0]);
            })
        },
        error: function(data) {
            if(data.responseJSON.error === 'No more posts' && firstload){
                $('#no-post').css('display','flex');
            }else{
                console.log(data.responseJSON.error);
            }
        }
    })
}

var showcomment=function(ele){
    var id= ele.getAttribute("data-post-id");
    $("#comment-form-submit").attr('data-post-id', id);
    $("#overlay").css("display", "flex");
    $("#comment-box ").css("display", "flex");
    $("#comment-box-content").html("");
    load_comment(ele);
    // $(".comment-form").attr('action',  "comment/" + id+"/");
}

$(document).ready(function() {
    csrf_token = $('#csrf_token').text();
    load_posts(0);
    username = document.getElementById('data-username').textContent;
    $(".hehe").click(function(){
        $(".comment-box").css("display", "none");
        $("#comment-feed").html("");
    })
    

    $('#comment-form-submit').on('click', function(event){
        event.preventDefault();
        var id= $(this).attr("data-post-id")
        var formdata= new FormData(document.getElementById('comment-form'));
        let ele = this;
        $.ajax({
            type:'POST',
            url: '/post/comment/' + id+'/',
            data: formdata,
            enctype: 'formdata', 
            processData: false,
            contentType: false,
            
            success: function(){
                $("#comment-box-content").html("");
                load_comment(ele);
                $("#comment-form textarea").val("");
                var val = parseInt($('#commentcount' + id).text());
                $('#commentcount' + id).text((val + 1) ? (val + 1).toString().replace(/^0+/, '') : 0);
            },
            error: function(){
    
            },
        })
    });
    
});

function initLikes(ele) {
    $(ele).on('click', function(e) {
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
                    $('#like' + id).addClass('svg-accent');
                    $('#like' + id).parent().find('p').addClass('text-accent');
                    var val = parseInt($('#likecount' + id).text());
                    $('#likecount' + id).text((val + 1).toString().replace(/^0+/, ''));
                } else if(data== 'unliked'){
                    $('#like' + id).removeClass('svg-accent');
                    $('#like' + id).parent().find('p').removeClass('text-accent');
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


var load_comment = function(ele) {
    var id= ele.getAttribute("data-post-id");
    $.ajax({
        url: '/post/load-comment/' + id,
        dataType: 'json',
        success: function(data) {
            Array.prototype.forEach.call(data, (comment) => {
                // console.log(JSON.parse(comment.content));
                var temp = document.getElementById("comment-template");
                var p = temp.content.cloneNode(true);
                p.querySelector('.comment-author').innerHTML = comment.author;
                // p.querySelector('.comment-date').innerHTML = comment.create_date;
                p.querySelector('.comment-content').innerHTML = comment.content;
                p.querySelector('.comment-author-img').setAttribute('src',comment.profile_img);
                document.getElementById('comment-box-content').appendChild(p);
                donotload = false;
            })
        },
        error: function(data) {
            console.log(data);
        }
    })
}

$('.create-post').click(function(e){
    $('#overlay').css('display','flex');
    $('#post-form-area').css('display','flex');
})

$('.comment-button').click(function(e){
    $('#overlay').css('display','flex');
    $('#comment-box').css('display','flex');
})