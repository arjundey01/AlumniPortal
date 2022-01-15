var curr_index = 1;
var donotload = false;
var firstload = true;
var username;
var csrf_token = ""

function parseHTML(data) {
    let str = ``;
    if(data["paragraph"])
        data["paragraph"].forEach((ele)=>{
            let fontSize = ele.text.length >= 120 ? 'sm':'lg';
            let px = ele.text.length >= 120 ? 'px-2' : 'px-4'
            str += `<p class="text-${fontSize} ${px} text-gray-500 mt-4 w-full text-justify">${ele.text}</p>`;
        });
    
    if(data["attaches"])
        data["attaches"].forEach((ele)=>{
            let size=ele.file.size/1024;
            let unit='KB';
            if(size>1023){
                size/=1024;
                unit='MB';
            }
            size=Math.round(size * 100) / 100;

            icon='file';
            if(['png','jpg','jpeg','svg'].includes(ele.file.extension))icon='png';
            else if(ele.file.extension=='pdf')icon='pdf';

            str += `<div class="post-attaches-wrapper mt-3 sm:mt-6 h-15 w-4/5 p-3 bg-gray-100 rounded flex items-center justify-between">		
                        <div class="flex items-center">
                            <img class = "h-10 w-10" src="/static/img/${icon}-icon.svg">
                            <div class = "ml-2">
                                <p class = "text-md text-gray-500 break-all">${ele.title}</p>
                                <p class = "text-sm text-gray-400">${size} ${unit}</p>
                            </div>
                        </div>
                        <a href="${ele.file.url}" class="flex-shrink-0">
                            <img class = "h-10 w-10" src="/static/img/dl-icon.svg">
                        </a>
                    </div>`;
        });
    
    if(data["image"])
        data["image"].forEach((ele)=>{
            str += `<div class="post-img-wrapper mt-3 sm:mt-6 w-full">
                        <img src="${ele.file.url}" class="w-full">
                        <!-- <span class="text-sm text-gray-400 italic mt-2">${ele.caption}</span> -->
                    </div>`;
        });
    return str;
}

function load_posts(index) {
    $.ajax({
        url: '/post/load-post/' + index,
        dataType: 'json',
        type: 'GET',
        data: {},
        success: function(data) {
            Array.prototype.forEach.call(data, (post) => {
                var temp = document.getElementById("post-template");
                var p = temp.content.cloneNode(true);
                p.id = 'post-' + post.id;
                $('.post-author', p).attr('href',`account/${post.author.username}`);
                $('.post-author-name', p).text(post.author.name);
                $('.post-author-desg', p).text(post.author.desg);
                $('.post-author-img', p).attr('src',post.author.profile_img)
                $('.post-date', p).text(post.datetime);
                $('.post-content', p).html(parseHTML(post.content));
                $('.like-count', p).text(post.like_count);
                $('.comment-count', p).text(post.comment_count);
                if (post.is_liked) {
                    $('.like-button svg', p).addClass('svg-accent');
                    $('.like-button p', p).addClass('text-accent');
                }
                $('.like-button', p).attr('data-post-id', post.id);
                $('.like-button svg', p).attr('id', 'like' + post.id.toString());
                $('.like-count', p).attr('id', 'likecount' + post.id.toString());
                $('.comment-count', p).attr('id', 'commentcount' + post.id.toString());
                $('.comment-button', p).on('click', function(){
                    showcomment(this);
                } );
                $('.post-likes', p).on('click', function(){
                    showLikes(this);
                } );
                if(username == post.author.username){
                    $('.post-options-button', p).removeClass('hidden');
                    $('.post-options-button', p).on('click', function(){
                        $('.post-options',this.parentElement).toggleClass('hidden');
                    } );
                    $('.post-delete', p).attr('data-id',post.id);
                    $('.post-delete', p).on('click',deletePost);
                }
                $('.comment-button', p).attr('data-post-id', post.id);
                $('.post-likes', p).attr('data-post-id', post.id);
                $('#feed').append(p);
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

function deletePost(e){
    const id = $(this).attr('data-id');
    const post = $(this).parents().eq(4);
    post.css('opacity','0.6');
    $(this).parent().toggleClass('hidden');
    $.ajax({
        type: 'POST',
        url: '/post/delete/',
        data: {id:id},
        success: (data)=>{
            console.log('Post deleted!');
            post.remove();
        },
        error: (err)=>{
            post.css('opacity','1');
        }
    })
}

function showcomment(ele){
    var id= ele.getAttribute("data-post-id");
    $("#comment-form-submit").attr('data-post-id', id);
    $("#overlay").css("display", "flex");
    $("#comment-box ").css("display", "flex");
    $("#comment-box-content").html("");
    load_comment(ele);
    // $(".comment-form").attr('action',  "comment/" + id+"/");
}

function showLikes(ele){
    var id= ele.getAttribute("data-post-id");
    $("#overlay").css("display", "flex");
    $("#likes-box ").css("display", "flex");
    $("#likes-box-content").html("");
    load_likes(ele);
    // $(".comment-form").attr('action',  "comment/" + id+"/");
}

$(document).ready(function() {
    csrf_token = $('#csrf_token').text();
    var id = $('#post-id').attr("data-id")
    console.log("post-id",id)
    load_posts(id);
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

var load_comment = function(ele) {
    var id= ele.getAttribute("data-post-id");
    $.ajax({
        url: '/post/load-comment/' + id,
        dataType: 'json',
        success: function(data) {
            if(data.length==0){
                $('#no-comment-msg').removeClass('hidden');
            }
            else{
                $('#no-comment-msg').addClass('hidden');
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
            }
        },
        error: function(data) {
            console.log(data);
        }
    })
}

var load_likes = function(ele) {
    var id= ele.getAttribute("data-post-id");
    $.ajax({
        url: '/post/load-likes/' + id,
        dataType: 'json',
        success: function(data) {
            if(data.length==0){
                $('#no-likes-msg').removeClass('hidden');
            }
            else{
                $('#no-likes-msg').addClass('hidden');
                Array.prototype.forEach.call(data, (like) => {
                    var temp = document.getElementById("like-template");
                    var p = temp.content.cloneNode(true);
                    p.querySelector('.like-author').innerHTML = like.author;
                    p.querySelector('.like-author-img').setAttribute('src',like.profile_img);
                    p.querySelector('.like-author-url').setAttribute('href','/account/'+like.username);
                    document.getElementById('likes-box-content').appendChild(p);
                })
            }
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