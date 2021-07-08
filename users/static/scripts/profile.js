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
        const id = $(this).attr('data-id');
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
            error: (data)=>{
                console.log('Could not change profile image.');
                $('.user-profile-img').attr('src',orgURL);
                $('#profile-img-upload-progress').css('width','0');
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
});