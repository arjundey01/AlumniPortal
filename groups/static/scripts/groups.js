$(document).ready(()=>{

});

$('.join-group').on('click',function(e){
    const id = $(this).attr('data-id');
    $.ajax({
        type: 'POST',
        url: `/groups/join-group/${id}/`,
        success: (data)=>{
            $(this).text('Joined');
            $(this).off('click');
            let ctr=$(`.member-count[data-id=${id}]`);
            let val=parseInt(ctr.text().split(" ")[0]);
            ctr.text(val+1 + " members");
        }
    })
});

$('.create-group').on('click',function(e){
    $('#overlay').css('display','flex');
    $('#create-group-form').css('display','flex');
})

$('#create-group-prev').on('click',function(e){
    $('#create-group-img').trigger('click');
})

$('#create-group-img').on('change',function(e){
    let img = $('#create-group-prev img');
    img.removeClass(['h-16', 'w-16']);
    img.addClass(['h-full', 'w-full']);
    previewImage(this, img[0]);
})

var previewImage= function(inputImg, prevImg){
    var reader = new FileReader();
    reader.onload = function(e) {
        $(prevImg).attr('src', e.target.result);
    }
    reader.readAsDataURL(inputImg.files[0]);
}

