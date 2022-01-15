let delete_btns = document.getElementsByClassName('delete-acc-btn')
let delete_btns2 = document.getElementsByClassName('delete-post-btn')
let delete_btns3 = document.getElementsByClassName('delete-group-btn')

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