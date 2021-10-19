$(document).ready(function(){
    $('.new-entry').on('click',function(e){
        $('#overlay').css('display','flex');
        const formarea = $(`#${$(this).attr('data-type')}-form-area`)[0];
        $(formarea).css('display','flex');
        $('form',formarea).attr('action', $('.add-url',formarea).val());
        $('input[name="pk"]', formarea).val("");
        $('.profile-form-submit',formarea).text('Add');
        $('form .profile-form-input',formarea).val("");
    });

    $('.update-entry').on('click',function(e){
        $('#overlay').css('display','flex');
        const type = $(this).attr('data-type');
        const id = $(this).attr('data-id')??'';
        const formarea = $(`#${type}-form-area`)[0];
        $(formarea).css('display','flex');
        $('form',formarea).attr('action', $('.update-url',formarea).val());
        $('.profile-form-submit',formarea).text('Update');
        $('input[name="pk"]', formarea).val(id);
        $('form .profile-form-input',formarea).each((ind,inp)=>{
            const val = $(`#${type}-${id}-${$(inp).attr('name')}`).text();
            console.log($(inp).attr('name'),val);
            if(val)
                $(inp).val(val);
        })
    });

    $('.delete-entry').on('click', function(e){
        $(this).parents().eq(3).css('opacity','0.5');
        $.ajax({
            type:'POST',
            url:$(this).attr('data-url'),
            data:{'pk':$(this).attr('data-id'), 'csrfmiddlewaretoken':$('#csrf-token').val()},
            success:(data)=>{
                $(this).parents().eq(3).remove();
            },
            error:(err)=>{
                console.log('Could not delete entry.');
                $(this).parents().eq(3).css('opacity','1');
            }
        });
    });

    $('#change-profile-img').on('click', function(e){
        $('#profile-img-inp').click();
    });

    $('#profile-img-inp').on('input change', function(e){
        if($(this).val()=="")return;
        const formData = new FormData($(this).parent()[0]);
        $('#profile-img-upload-progress').css('width','100%');
        const orgURL = $('.user-profile-img').attr('src');
        previewImage(this,'.user-profile-img');
        $('#profile-img-change-status').text('Uploading...');
        $.ajax({
            xhr: function() {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", function(evt) {
                    if (evt.lengthComputable) {
                        var percentComplete = (evt.loaded / evt.total) * 100;
                        $('#profile-img-upload-progress').css('width',(100-percentComplete)+'%');
                    }
                }, false);
                return xhr;
            },
            type: 'POST',
            url: '/account/change-profile-img/',
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: (data)=>{
                $('#profile-img-change-status').text('Click to Change');
            },
            error: (data)=>{
                console.log('Could not change profile image.');
                $('.user-profile-img').attr('src',orgURL);
                $('#profile-img-upload-progress').css('width','0');
                $('#profile-img-change-status').text('Click to Change');
            }
        });
    })

    var previewImage= function(inputImg, prevImg){
        var reader = new FileReader();
        reader.onload = function(e) {
            $(prevImg).attr('src', e.target.result);
        }
        reader.readAsDataURL(inputImg.files[0]);
    }


    $('.sugg-inp input').on('focus', function(){
        $(this).parent().find('.sugg-inp-sugg-wrp').removeClass('hidden');
    });
    
    $('.sugg-inp input').on('focusout', function(){
        setTimeout(()=>{
            $(this).parent().find('.sugg-inp-sugg-wrp').addClass('hidden');
        },250);
    });

    $('.sugg-inp input').on('keyup', function(){
        const suggs = $(this).parent().find('.sugg-inp-sugg');
        const val = $(this).val();
        if(val==""){
            $(this).parent().find('.sugg-inp-msg').text('Click to Choose');
            suggs.removeClass('hidden');
            return;
        }
        let empty = true;
        suggs.addClass('hidden');
        suggs.each((ind,sugg)=>{
            if($(sugg).text().startsWith(val)){
                $(sugg).removeClass('hidden');
                empty = false;
            }
        });
        if(empty)
            $(this).parent().find('.sugg-inp-msg').text('No results');
        else
            $(this).parent().find('.sugg-inp-msg').text('Click to Choose');
    });

    $('.sugg-inp-sugg').on('click', function(){
        $(this).parents().eq(2).find('input').val($(this).text().trim());
    });
});