$(document).ready(()=>{
    if(location.hash!=""){
        var lt=location.hash.substring(1);
        console.log(lt);
        $(".nav-link[href='#"+lt+"']").click();
    }
})

$('#user-exp').on('click',function(e){
    $('.user-experience').removeClass('hidden');
    $(this).addClass('hidden');
})
$('#user-extrajob').on('click',function(e){
    $('.user-jobs').removeClass('hidden');
    $(this).addClass('hidden');
}) 

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
    $(".update_ex_form #id_experience").val($(`p[data-id=exp${$(this).attr("data-update-id")}]`).text());
    $(".update_ex_form #id_start_date").attr("placeholder",$(`div[data-id=exstart${$(this).attr("data-update-id")}]`).text());
    $(".update_ex_form #id_end_date").attr("placeholder",$(`div[data-id=exend${$(this).attr("data-update-id")}]`).text());
})
$(".edit-job").click(function(ele){
    $("#overlay").css('display', 'flex');
    $(".update_ex_form").css('display', 'none');
    $(".update_job_form").css('display','flex');
    $(".add_experience").css('display','none');
    $(".add_job").css('display', 'none');
    $(".update_job_form").attr('action', 'update/job/'+ $(this).attr("data-update-id")+'/');
    //$(".update_job_form input[type=text]").val($(".user-job", $(this).parent()).text());
    $(".update_job_form #id_organization").val($(`div[data-id=org${$(this).attr("data-update-id")}]`).text());
    $(".update_job_form #id_description").val($(`div[data-id=description${$(this).attr("data-update-id")}]`).text());
    $(".update_job_form #id_designation").val($(`div[data-id=title${$(this).attr("data-update-id")}]`).text());
    //$(".update_job_form #id_start_date").val($(`div[data-id=start${$(this).attr("data-update-id")}]`).text());
    //$(".update_job_form #id_end_date").val($(`div[data-id=end${$(this).attr("data-update-id")}]`).text());
    $(".update_job_form #id_end_date").attr("placeholder",$(`div[data-id=end${$(this).attr("data-update-id")}]`).text());
    $(".update_job_form").attr("data-id",$(this).attr("data-update-id"))
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
editing=function(){
    window.location.replace("http://localhost:8000/details/");
}
