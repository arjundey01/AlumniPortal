$(document).ready(()=>{
    if(location.hash!=""){
        var lt=location.hash.substring(1);
        console.log(lt);
        $(".nav-link[href='#"+lt+"']").click();
    }
})

// $(".update-close").click(function(){
//     {
//     $(".overlay").css("display", "none");
//     }
// })        

$('#user-exp').on('click',function(e){
    $('.user-experience').removeClass('hidden');
    $(this).addClass('hidden');
})
$('#user-extrajob').on('click',function(e){
    $('.user-jobs').removeClass('hidden');
    $(this).addClass('hidden');
}) 

// $(".pedit").click(function(ele){
//     {
//     // var id = $(this).attr("data-update-id")
//     $(".overlay").css('display', 'block');
//     $(".update_form").css('display', 'none');
//     $(".update_edu_form").css('display', 'none');
//     $(".update_p_form").css('display', 'block');
//     $(".update_p_form").attr('action', 'update/project/'+ $(this).attr("data-update-id")+'/');
//     console.log($(".user-project", $(this).parent()).text());
//     $(".update_p_form input[type=text]").val($(".user-project", $(this).parent()).text());
//     }
// })

// $(".eduedit").click(function(ele){
//     {
//     // var id = $(this).attr("data-update-id")
//     $(".overlay").css('display', 'block');
//     $(".update_form").css('display', 'none');
//     $(".update_p_form").css('display', 'none');
//     $(".update_j_form").css('display','none');
//     $(".update_edu_form").css('display', 'block');
//     $(".update_edu_form").attr('action', 'update/education/'+ $(this).attr("data-update-id")+'/');
//     console.log($(".user-edu", $(this).parent()).text());
//     $(".update_edu_form input[type=text]").val($(".user-edu", $(this).parent()).text());
//     }
// })

// $("#new_experience").click(function(){
// if($(this).attr("val") == "show")
//     {
//     $(".experience_form").css('display', 'block');
//     $("#new_experience").html('<span>&#8722;</span>');
//     $(this).attr("val","hide");
//     }
// else
//     {
//     $(".experience_form").css('display', 'none');
//     $("#new_experience").html('<span>&#43;</span>');
//         $(this).attr("val","show");
//     }
// })

// $("#new_project").click(function(){
// if($(this).attr("val") == "show")
//     {
//     $(".project_form").css('display', 'block');
//     $("#new_project").html('<span>&#8722;</span>');
//     $(this).attr("val","hide");
//     }
// else
//     {
//     $(".project_form").css('display', 'none');
//     $("#new_project").html('<span>&#43;</span>');
//         $(this).attr("val","show");
//     }
// })
// $("#new_education").click(function(){
// if($(this).attr("val") == "show")
//     {
//     $(".education_form").css('display', 'block');
//     $("#new_education").html('<span>&#8722;</span>');
//     $(this).attr("val","hide");
//     }
//     else
//     {
//     $(".education_form").css('display', 'none');
//     $("#new_education").html('<span>&#43;</span>');
//         $(this).attr("val","show");
//     }
// })

// $("#new_job").click(function(){
// if($(this).attr("val") == "show")
//     {
//     $(".pastJobs_form").css('display', 'block');
//     $("#new_job").html('<span>&#8722;</span>');
//     $(this).attr("val","hide");
//     }
//     else
//     {
//     $(".pastJobs_form").css('display', 'none');
//     $("#new_job").html('<span>&#43;</span>');
//         $(this).attr("val","show");
//     }
// })
// $(".del-item-btn").click(function(){
// let id = $(this).attr('data-delete-id');
// let type = $(this).attr('data-type');
// location.href = 'delete/' + type + '/' + id;
// })

// $("#new_experience").click(function(){
// if($(this).attr("val") == "show")
//     {
//     $(".add_experience").css('display', 'block');
//     $("#new_experience").html('<span>&#8722;</span>');
//     $(this).attr("val","hide");
//     }
// else
//     {
//     $(".add_experience").css('display', 'none');
//     $("#new_experience").html('<img class="h-2 inline" src="/static/img/add.svg" alt="+">');
//         $(this).attr("val","show");
//     }
// })
$("#new_job").click(function(){
    $("#overlay").css('display', 'flex');
    $(".add_experience").css('display','none');
    $(".update_ex_form").css('display', 'none');
    $(".update_job_form").css('display','none');
    $(".add_job").css('display', 'flex');
})
$("#new_experience").click(function(){
    $("#overlay").css('display','flex');
    $(".add_experience").css('display','block');
    $(".add_job").css('display', 'none');
    $(".update_ex_form").css('display', 'none');
    $(".update_job_form").css('display','none');
}) 
$(".edit").click(function(ele){
    $("#overlay").css('display', 'flex');
    $(".update_ex_form").css('display', 'block');
    $(".update_job_form").css('display','none');
    $(".add_experience").css('display','none');
    $(".add_job").css('display', 'none');
    $(".update_ex_form").attr('action', 'update/experience/'+ $(this).attr("data-update-id")+'/');
    $(".update_ex_form input[type=text]").val($(".user-experience", $(this).parent()).text());
})
$(".edit-job").click(function(ele){
    $("#overlay").css('display', 'flex');
    $(".update_ex_form").css('display', 'none');
    $(".update_job_form").css('display','flex');
    $(".add_experience").css('display','none');
    $(".add_job").css('display', 'none');
    $(".update_job_form").attr('action', 'update/job/'+ $(this).attr("data-update-id")+'/');
    $(".update_job_form input[type=text]").val($(".user-job", $(this).parent()).text());
})
$(".del-exp-btn").click(function(){
let id = $(this).attr('data-delete-id');
let type = $(this).attr('data-type');
location.href = 'delete/' + type + '/' + id;
})
$(".del-job-btn").click(function(){
    let id = $(this).attr('data-delete-id');
    let type = $(this).attr('data-type');
    location.href = 'delete/' + type + '/' + id;
})
