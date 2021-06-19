let curr_index = 1;
let donotload = false;
let firstload = true;
let username;
let csrf_token = ""

const reload_js = src => {
  $('script[src="' + src + '"]').remove();
  $('<script>').attr('src', src).appendTo('head');
}

$(document).ready(function () {
  csrf_token = $("#csrf_token").text();
  load_question(0);

  $("#ask_button").click(function (e) {
    e.preventDefault();
    $("#question_form").submit();
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

        // clone node of the subtree of the question template
        let question_clone =
          question_template.content.cloneNode(true);

        // set the id
        question_clone.id = "question-" + question.id;

        // modify the data for .question-content and .question-author within the clone node
        question_clone.querySelector(
          ".question-content"
        ).innerHTML = question.content;
        question_clone.querySelector(
          ".question-author"
        ).innerHTML = question.author.name;
        question_clone.querySelector(
            ".question-author"
        ).href = `../account/${question.author.username}/`
        question_clone.querySelector(
          ".question-details"
        ).href = `${question.id}/`

        if(Object.keys(question.answers).length != 0) {
          // template of answer
          let answer_template = document.getElementById("answer-template");
  
          // clone node of subtree of the answer template
          let answer_clone = answer_template.content.cloneNode(true);
  
          // modify the data for answer
          answer_clone.querySelector(
            ".ans-img"
          ).src = question.answers.profile_img;
          answer_clone.querySelector(
            ".ans-author"
          ).innerHTML = question.answers.name
          answer_clone.querySelector(
            ".ans-content"
          ).innerHTML = question.answers.content
  
          question_clone.querySelector(
            ".answer-container"
          ).appendChild(answer_clone)
        }

        // append the clone to #question-container
        document
          .getElementById("question-container")
          .appendChild(question_clone);
      }
      reload_js('/static/scripts/base.js'); // reload the base js to add events

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
