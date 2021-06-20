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
    if($("#question-text").val().length === 0) alert("Sorry, the question can't be empty!");
    else { 
      $("#question_form").submit();
    }
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

        // clone node of the subtree of the question template
        let question_clone = $("#question-template").contents().clone(true);

        // set the id
        question_clone.attr("id", `question-${question.id}`);

        // modify the data for .question-content and .question-author within the clone node
        $(".question-content", question_clone).html(question.content);
        $(".question-author", question_clone).html(question.author.name);
        $(".question-author", question_clone).attr("href", `../account/${question.author.username}`);
        $(".question-details", question_clone).attr("href", `${question.id}/`);
        if(Object.keys(question.answers).length != 0) {
          // clone node of subtree of the answer template
          let answer_clone = $("#answer-template").contents().clone(true);
  
          // modify the data for answer
          $(".ans-img", answer_clone).attr("src", question.answers.profile_img);
          $(".ans-author", answer_clone).html(question.answers.name);
          $(".ans-content", answer_clone).html(question.answers.content);
          
          // append answer_clone to question_clone
          $(".answer-container", question_clone).append(answer_clone)
        }

        // append question_clone to #question-container
        $("#question-container").append(question_clone);
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
