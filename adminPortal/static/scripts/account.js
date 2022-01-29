let delete_btns = document.getElementsByClassName('delete-acc-btn')
let delete_btns2 = document.getElementsByClassName('delete-post-btn')
let delete_btns3 = document.getElementsByClassName('delete-group-btn')
let csrf_token = $('#csrf-token').val();

for (var i = 0; i < delete_btns.length; i++){
    delete_btns[i].addEventListener("click",function(){
        var acc_id;
        acc_id = $(this).attr("data-acc-id")
        var acc_name;
        acc_name = $(this).attr("data-acc-name")
        if (confirm('Are you sure you want to delete the Account of '+acc_name)) {
          $.ajax({
            type: "GET",
            url: "/admin/accounts/delete/"+acc_id,
            success: function (data) {
              if(data.status==200){
                window.location.reload()
              } else {
                alert(data.message)
              }
            },
            error: function (data) {
              alert(data);
            },
          });
          
          } else {
            
          }
    })
}
for (var i = 0; i < delete_btns2.length; i++){
    delete_btns2[i].addEventListener("click",function(){
        var post_id;
        post_id = $(this).attr("data-post-id")
        var post_name;
        post_name = $(this).attr("data-post-name")
        if (confirm('Are you sure you want to delete this Post of '+post_name)) {
          $.ajax({
            type: "GET",
            url: "/admin/posts/delete/"+post_id,
            success: function (data) {
              if(data.status==200){
                window.location.reload()
              } else {
                alert(data.message)
              }
            },
            error: function (data) {
              alert(data);
            },
          });
          
          } else {
            
          }
    })
}
for (var i = 0; i < delete_btns3.length; i++){
    delete_btns3[i].addEventListener("click",function(){
      console.log("btn clicked")
        var group_id;
        group_id = $(this).attr("data-group-id")
        var group_name;
        group_name = $(this).attr("data-group-name")
        if (confirm('Are you sure you want to delete this group named : '+group_name)) {
          $.ajax({
            type: "GET",
            url: "/admin/groups/delete/"+group_id,
            success: function (data) {
              if(data.status==200){
                window.location.reload()
              } else {
                alert(data.message)
              }
            },
            error: function (data) {
              alert(data);
            },
          });
          
          } else {
            
          }
    })
}

$('.delete-faq-btn').on('click', function(e){
  let id = $(this).attr('data-faq-id');
  if (confirm('Are you sure you want to delete the question?')) {
      window.open(`/admin/faqs/delete/${id}/`,"_self");
  }
});

$('.delete-event-btn').on('click', function(e){
  let id = $(this).attr('data-event-id');
  if (confirm('Are you sure you want to delete the question?')) {
      window.open(`/admin/events/delete/${id}/`,"_self");
  }
});


//=================POSTS====================

$('.view-post').click(function(e){
  $('#overlay').css('display','flex');
  let id = $(this).attr('data-id');
  $.ajax({
    url: '/post/load-post/' + id,
    dataType: 'json',
    type: 'POST',
    data: {'csrfmiddlewaretoken':csrf_token},
    success: function(post) {
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
        $('#post-view-container').html('');
        $('#post-view-container').append(p);
    },
    error: function(data) {
        alert('Failed to load. Please reload the page and try again.')
    }
  })
});

$('.close-overlay').click(function(e){
  $('#overlay').css('display','none');
});

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

//====================GROUPS===========
$('.create-group').click(function(e){
  $('#overlay').css('display','flex');

  let grpForm = $('#create-group-form')[0];
  let url = $(grpForm).attr('action');
  $(grpForm).attr('action',url.split("?")[0]);

  $('.form-title', grpForm).text("Create a Group");
  $('input[type=submit]', grpForm).val("Create");

  $('input[name=title]', grpForm).val("");
  $('textarea[name=description]', grpForm).val("");
  $('input[name=cover_image]', grpForm).attr('src',"");
  $('input[name=cover_image]', grpForm).attr('value',"");
  let img = $('#create-group-prev img');
  img.parent().find('p').show();
  img.attr('src', '/static/img/add.svg');
  img.addClass(['h-16', 'w-16']);
  img.removeClass(['h-full', 'w-full']);
});

$('.edit-group-btn').click(function(e){
  $('#overlay').css('display','flex');
  let grpRow = $(this).parent().parent()[0];
  let id = $(this).attr('data-group-id');

  let grpForm = $('#create-group-form')[0];
  let url = $(grpForm).attr('action');
  $(grpForm).attr('action',url+`?id=${id}`);

  $('.form-title', grpForm).text("Edit Group");
  $('input[type=submit]', grpForm).val("Submit");

  $('input[name=title]', grpForm).val($('.group-title',grpRow).text());
  $('textarea[name=description]', grpForm).val($('.group-desc',grpRow).text());
  
  let imgSrc = $('.group-image',grpRow).attr('src');
  $('input[name=cover_image]', grpForm).attr('src',imgSrc);
  let img = $('#create-group-prev img');
  img.parent().find('p').hide();
  img.attr('src', imgSrc);
  img.removeClass(['h-16', 'w-16']);
  img.addClass(['h-full', 'w-full']);
});


$('#create-group-prev').on('click',function(e){
  $('#create-group-img').trigger('click');
})

$('#create-group-img').on('change',function(e){
  let img = $('#create-group-prev img');
  img.removeClass(['h-16', 'w-16']);
  img.addClass(['h-full', 'w-full']);
  img.parent().find('p').hide();
  previewImage(this, img[0]);
})

var previewImage= function(inputImg, prevImg){
  var reader = new FileReader();
  reader.onload = function(e) {
      $(prevImg).attr('src', e.target.result);
  }
  reader.readAsDataURL(inputImg.files[0]);
}