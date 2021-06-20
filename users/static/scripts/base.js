let loadAccordion = () => {
    $('.accordion-question').click(function(e){
        
        let entry = $(this).parent();
        if(entry.hasClass('accordion-entry-collapsed')){
            expand(entry);
            $('.accordion-entry', entry.parent()).each(function(ind,ele){
                // console.log($(ele),entry);
                if(!$(ele).is(entry)){
                    collapse($(ele));
                }
            })
        }else{
            collapse(entry);
        }
    
        function expand(ele){
            let ans = ele.find('.accordion-answer')[0];
            let p=ans.querySelector('p');
            let contentHeight = (p.clientHeight + 2*parseInt($(p).css('margin').replace('px', ''))) + 'px';
            ele.removeClass('accordion-entry-collapsed');
            ans.style.height=contentHeight;
            setTimeout(()=>{ans.style.height='auto';},500);
        }
        function collapse(ele){
            let ans = ele.find('.accordion-answer')[0];
            let p=ans.querySelector('p');
            let contentHeight = (p.clientHeight + 2*parseInt($(p).css('margin').replace('px', ''))) + 'px';
            ans.style.height=contentHeight;
            setTimeout(()=>{ans.style.height=0;},10);
            ele.addClass('accordion-entry-collapsed')
        }
    });
};

$(document).ready(()=>{
    if($('.chatbox-header').length){
        other=document.querySelector('#other-member').textContent;
        getLastActive(other,10);
    }
    //getOnline(15);
    $('.chat-button').click(startChat);
    $('.follow-button').click(follow);

    loadAccordion();

    $('#sidebar-btn').click(function(e){
        let state = $(this).attr('data-toggle');
        if(state === 'on'){
            $('.sidebar').removeClass('sidebar-active');
            $(this).attr('data-toggle','off');
        }else{
            $('.sidebar').addClass('sidebar-active');
            $(this).attr('data-toggle','on');
        }
    });

    $('#close-overlay').click(function(e){
        $('#overlay').css('display','none');
        $('#overlay').children().each((ind,ele)=>{
            if(ele.id !== 'close-overlay')
                ele.style.display = 'none';
        })
    });

    $("[contenteditable]").focusout(function(){      
        if (!$(this).text().trim().length) {
            $(this).empty();
        }
    });
});

var updateOnlinePanel=function(data){
    let users=Array();
    data.forEach((ele)=>{
        users.push(ele.username);
        if($(`.online-user span[data-user="${ele.username}"]`).length)return;
        let online_panel=$('#online-panel')[0]
        let temp = document.getElementById("tmp-online-user");
        let p = temp.content.cloneNode(true);
        p.querySelector("span").innerHTML=ele.name;
        p.querySelector("a img").src=ele.profile_img_url;
        p.querySelector("span").setAttribute("data-user",ele.username)
        p.querySelectorAll("a")[0].setAttribute('href','/account/'+ele.username);
        $("img:last-of-type",p).attr('data-other',ele.username);
        $("img:last-of-type",p).click(startChat);
        online_panel.appendChild(p);
    })
    $(`.online-user`).each((ind,ele)=>{
        let name=ele.querySelector("span").getAttribute("data-user");
        if(!users.includes(name)){
            ele.remove();
        }
    })
}
var getOnline=function(interval){
    (function(){
        $.ajax({
            type:"GET",
            url:'/chat/online/',
            dataType:'json',
            success: function(data){
                //console.log(data);
                if($('#online-panel').length){
                    updateOnlinePanel(data);
                }
            }
        })
        setTimeout(arguments.callee, interval*1000);
    })();
}

var getLastActive=function(username,interval){
    (function(){
        $.ajax({
            type:"GET",
            url:'/chat/last-active/',
            data:{'username':username},
            success: function(data){
                if($('.chatbox-header').length){
                    // console.log(data);
                    $('.chatbox-header span').text(data);
                }
            }
        })
        setTimeout(arguments.callee, interval*1000);
    })();
}

var startChat=function(ele){
    let user=$(this).attr("data-self");
    let other=$(this).attr("data-other");
    let csrf=$(this).attr("data-csrf");
    let formData= new FormData();
    formData.append("csrfmiddlewaretoken",csrf);
    // console.log(other);
    formData.append("member",other);
    if(user!=""){
        $.ajax({ 
            type:"POST", 
            url: '/chat/start/', 
            data: formData, 
            processData: false,
            contentType: false,
            success: function(loc){
                window.location=loc;
            },
            error: function(e,exc) 
            {
                console.error(exc);
            }
        })   
    }
}

var follow=function(ele){
    let username= $(this).attr("data-username");
    $.ajax({ 
        type:"GET", 
        url: '/follow/', 
        data: {"username":username}, 
        success: function(data){
            $(`.follow-button[data-username="${username}"]`).removeClass('fa-plus');
            $(`.follow-button[data-username="${username}"]`).addClass('fa-check');
            $(`.follow-button[data-username="${username}"]`).removeClass('follow-button');
        },
        error: function(e,exc) 
        {
            console.error(exc);
        }
    })   
}

