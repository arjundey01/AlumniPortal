let curr_index = 1;
let donotload = false;
let firstload = true;
let username;
let csrf_token = ""

$(document).ready(function () {
  csrf_token = $("#csrf_token").text();
  load_question(0);

  $("#ask_button").click(function (e) {
    e.preventDefault();
    $("#question_form").submit();
    /*if ($("#ask_text").html() === "") {
            alert("Enter some text first!");
            return;
        }
        let formdata = new FormData(document.getElementById("question_form"));
        // for (var pair of formdata) {
        //     console.log(pair[0] + ": " + pair[1]);
        // }
        $.ajax({
            type: "POST",
            url: "/faq/create-question/",
            data: formdata,
            processData: false,
            contentType: false,
            enctype: "multipart/form-data",
            success: function (response) {
                // clear the question-text input's value
                console.log("Question Posted!")
                $("#question-text").val("");
                load_question();
            }
        });*/
  });
});

let load_question = function (index) {
  let tags = [];
  $('.feed-tag').each((ind,ele)=>{
      if(ele.textContent.length)
          tags.push(ele.textContent);
  });
  $.ajax({
    type: "POST",
    url: "/faq/load-question/" + index,
    data: {'tags': JSON.stringify(tags), 'csrfmiddlewaretoken': csrf_token },
    dataType: "json",
    success: function (data) {
      for(let question of data) {
        // []. is shorthand for Array.prototype. //
        // instead we can also do [].forEach.call(data, (question) => {...}); too.

        // template of the question.
        let question_template = document.getElementById("question-template");

        // clone node of the subtree of the template
        let question_template_children_clone =
          question_template.content.cloneNode(true);

        // set the id
        question_template_children_clone.id = "question-" + question.id;

        // modify the data for .question-content and .question-author within the clone node
        question_template_children_clone.querySelector(
          ".question-content"
        ).innerHTML = question.content;
        question_template_children_clone.querySelector(
          ".question-author"
        ).innerHTML = question.author.name;
        question_template_children_clone.querySelector(
            ".question-author"
        ).href = `../account/${question.author.username}`

        // append the clone to #question-container
        document
          .getElementById("question-container")
          .appendChild(question_template_children_clone);
      }

      donotload = false;
      firstload = false; // tells that initial posts have been loaded.
    },
    error: function (data) {
        if(data.responseJSON.error === 'No more posts' && firstload){
            $('#no-post').css('display','flex');
        }else{
            console.log(data.responseJSON.error);
        }
    },
  });
};

$(window).scroll(function() {
    //console.log($(window).scrollTop(),$(document).height() , $(window).height())
    if ($(window).scrollTop() > $(document).height() - $(window).height() - 50 && !donotload) {
        load_question(curr_index);
        curr_index += 1;
        donotload = true;
    }
});
