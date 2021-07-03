$(document).ready(function(){

    //====================================UI=======================================

    $('#post-textarea').on('input', function(e){
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    })

    $('#post-add-image').on('click', function(e){
        if($(this).attr('data-active')=='0')return;
        $('#post-image-input').trigger('click');
    })

    $('#post-image-prev').on('click', function(e){
        $('#post-image-input').val("");
        $('#post-add-image').removeClass('opacity-50');
        $('#post-add-image').attr('data-active',1);
        $('#post-image-prev').addClass('hidden');
    })

    $('#post-image-input').on('change',function(e){
        console.log(this.value);
        if(this.value !== ""){
            let img = $('#post-image-prev');
            img.removeClass(['hidden']);
            previewImage(this, img[0]);
            $('#post-add-image').addClass('opacity-50');
            $('#post-add-image').attr('data-active',0);
            console.log("changed");
        }
    })

    const previewImage= function(inputImg, prevImg){
        var reader = new FileReader();
        reader.onload = function(e) {
            $(prevImg).attr('src', e.target.result);
        }
        reader.readAsDataURL(inputImg.files[0]);
    }

    $('#post-add-attach').on('click', function(e){
        if($(this).attr('data-active')=='0')return;
        let clicked = false;
        $('.post-file-input').each(function(i,ele){
            if(!clicked && $(this).val() == ""){
                $(this).trigger('click');
                clicked=true;
            }
        })
    })
    
    $('.post-file-input').on('change',function(e){
        if(this.files[0].size>11*1024*1024){
            alert('File size limit exceeded. Please attach a smaller file (<=10MB).')
            this.value="";
        }else{
            previewAttach(this);
        }
        let avl = 0;
        $('.post-file-input').each(function(i,ele){
            if($(this).val()=="")
                avl++;
        })
        $('#post-rem-attach').text(avl);
        if(!avl){
            $('#post-add-attach').addClass('opacity-50');
            $('#post-add-attach').attr('data-active',0);
        }
    })

    const previewAttach=(input)=>{
        const file = input.files[0];
        const temp = $("#attach-prev-temp")[0];
        let p = temp.content.cloneNode(true);

        let ext = file.name.split('.');
        let name=ext[0];
        ext = ext[ext.length-1];

        let size=file.size/1024;
        let unit='KB';
        if(size>1023){
            size/=1024;
            unit='MB';
        }

        let type='file';
        if(file.type == 'application/pdf')type='pdf';
        if(file.type.startsWith('image'))type='png';
        size=Math.round(size * 100) / 100;

        $('.attach-title',p).text(name);
        $('.attach-size',p).text(size+" "+unit);
        $('.attach-thumb',p).attr('src',`/static/img/${type}-icon.svg`);
        $('.attach-remove',p).attr('data-input',input.id);
        $('.attach-remove',p).on('click',function(e){removeAttach(this)});
        $('#post-attach-prev').append(p);
    }

    const removeAttach = (attach)=>{
        $(`#${$(attach).attr('data-input')}`).val("");
        $(attach).parent().remove();
        $('#post-add-attach').removeClass('opacity-50');
        $('#post-add-attach').attr('data-active',1);
        let ctr = $('#post-rem-attach');
        ctr.text(parseInt(ctr.text())+1);
    }



    //===============================UPLOAD AND SUBMISSION===========================
    
    const postContentInp = $('#post-form textarea');
    const postContent = {'paragraph':[],'image':[],'attaches':[]};

    $('#post-form-submit').click(function(){
        //If there are no files to upload, submit immediately
        let attaches_size=$('.post-file-input').filter(function(){return this.value!=="";}).length;
        let images_size=$('#post-image-input').filter(function(){return this.value!=="";}).length;
       
        if(attaches_size + images_size == 0){
            postContent['paragraph'].push({'text':$('#post-textarea').val()});
            postContentInp.val(JSON.stringify(postContent));
            $('#post-form').submit();
            return;
        }

        let ctr=0;

        $('.post-file-input').each((ind,ele)=>{
            if(ele.value == "")return;
            fd = new FormData();
            fd.append("file", ele.files[0], ele.files[0].name);
            fd.append("size",ele.files[0].size);
            $.ajax({
                type: "POST",
                url:'/post/fileUpload/',
                data: fd,
                processData: false,
                contentType: false,
                success: function(data){
                    console.log(data);
                    ctr++;
                    let attach={}
                    attach['file']=data.file;
                    attach['title']=ele.files[0].name;
                    postContent['attaches'].push(attach);

                    if(ctr==attaches_size+images_size){
                        console.log('done');
                        postContent['paragraph'].push({'text':$('#post-textarea').val()});
                        postContentInp.val(JSON.stringify(postContent));
                        $('#post-form').submit();
                    }
                }
            })
        });
        $('#post-image-input').each((ind,ele)=>{
            if(ele.value == "")return;
            fd = new FormData();
            fd.append("image", ele.files[0], ele.files[0].name);
            $.ajax({
                type: "POST",
                url:'/post/imageUpload/',
                data: fd,
                processData: false,
                contentType: false,
                success: function(data){
                    console.log(data);
                    ctr++;
                    let image={}
                    image['file']=data.file;
                    image['title']=ele.files[0].name;
                    postContent['image'].push(image);

                    if(ctr==attaches_size+images_size){
                        console.log('done');
                        postContent['paragraph'].push({'text':$('#post-textarea').val()});
                        postContentInp.val(JSON.stringify(postContent));
                        $('#post-form').submit();
                    }
                }
            })
        });
    });


    //======================================TAGS====================================
    
    const selTags=[];
    
    $('#post-form select').css('display','none');
    $('#post-form option').each((i,e)=>{e.selected=false;});
    $('.feed-tag').each((ind,ele)=>{
        gID = $(ele).attr('data-id');
        if(gID){
            selTags.push(gID);
            $(`#post-form select option[value=${gID}]`)[0].selected = true;
        }
    })

    if(!selTags.length){
        let tagId;
        try {
            tagId=JSON.parse($('#tag-list').text());
        } catch (error) {
            tagId={};
        }
        console.log(tagId);
        let tagList=[];
        for(let tag in tagId)tagList.push(tag);
        tagList.sort();
        $('#tag-input').on('input',function(){
            let val = $(this).val();
            if(val===""){
                $('#tag-sugg-cmp').text("");
                $('#tag-sugg-inc').text("");
                $('#no-tag-msg').css('display','none');
                return;
            }
            let res = tagList.find(ele=>ele.toLowerCase().startsWith(val.toLowerCase()));
            if(!res){
                $('#no-tag-msg').css('display','block');
                return;
            }
            $('#no-tag-msg').css('display','none');
            let cmp = res.slice(0,val.length);
            let inc = res.slice(val.length, res.length);
            $('#tag-sugg-cmp').text(cmp);
            $('#tag-sugg-inc').text(inc);
        })

        $('#tag-input').on('keypress',function(e){
            if(e.which==13 || e.which==9){
                e.preventDefault();
                let temp =$("#tag-temp")[0];
                let tag = temp.content.cloneNode(true);
                let val = $('#tag-input').val();
                let res = tagList.find(ele=>ele.toLowerCase().startsWith(val.toLowerCase()));
                if(!res)return;
                tagList.splice(tagList.indexOf(res),1);
                $('p',tag).text(res);
                $('.tag-remove',tag).click(function(e){
                    let parent = $(this).parent()[0];
                    let delTag = $('p',parent).text();
                    tagList.push(delTag);
                    tagList.sort();
                    selTags.splice(selTags.indexOf(delTag),1);
                    $(`#post-form select option[value=${tagId[delTag]}]`)[0].selected = false;
                    $(parent).remove();
                })
                $('#tags').append(tag);
                selTags.push(res);
                $(`#post-form select option[value=${tagId[res]}]`)[0].selected = true;
                $('#tag-input').val("");
                $('#tag-sugg-cmp').text("");
                $('#tag-sugg-inc').text("");
                $('#no-tag-msg').css('display','none');
            }
        })
    }
    else{
        $('#tag-search-form').css('display','none');
    }

})