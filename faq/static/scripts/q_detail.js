let upvote_btns = document.getElementsByClassName("upvote-btn");
let downvote_btns = document.getElementsByClassName("downvote-btn");
let accept_btns = document.getElementsByClassName("accept-btn");

for (var i = 0; i < upvote_btns.length; i++) {
  upvote_btns[i].addEventListener("click", function () {
    var ans_id;
    ans_id = $(this).attr("data-answer-id");
    $.ajax({
      type: "GET",
      url: "/faq/upvote",
      data: {
        answer_id: ans_id,
      },
      success: function (data) {
        console.log(data);
        if (data == "added_upvote") {
          $("#upvote-btn-" + ans_id).addClass("svg-accent-u");
          $("#upvote-value-" + ans_id).addClass("text-accent");
          var val = parseInt($("#upvote-value-" + ans_id).text());
          $("#upvote-value-" + ans_id).text((val + 1).toString());
        } else if (data == "removed_downvote_and_added_upvote") {
          $("#upvote-btn-" + ans_id).addClass("svg-accent-u");
          $("#upvote-value-" + ans_id).addClass("text-accent");
          var val = parseInt($("#upvote-value-" + ans_id).text());
          $("#upvote-value-" + ans_id).text((val + 1).toString());
          $("#downvote-btn-" + ans_id).removeClass("svg-accent-d");
          $("#downvote-value-" + ans_id).removeClass("text-accent");
          var val = parseInt($("#downvote-value-" + ans_id).text());
          $("#downvote-value-" + ans_id).text((val - 1).toString());
        } else if (data == "removed_upvote") {
          $("#upvote-btn-" + ans_id).removeClass("svg-accent-u");
          $("#upvote-value-" + ans_id).removeClass("text-accent");
          var val = parseInt($("#upvote-value-" + ans_id).text());
          $("#upvote-value-" + ans_id).text((val - 1).toString());
        }
      },
      error: function (data) {
        alert(data);
      },
    });
  });
}
for (var i = 0; i < downvote_btns.length; i++) {
  downvote_btns[i].addEventListener("click", function () {
    var ans_id;
    ans_id = $(this).attr("data-answer-id");
    $.ajax({
      type: "GET",
      url: "/faq/downvote",
      data: {
        answer_id: ans_id,
      },
      success: function (data) {
        console.log(data);
        if (data == "added_downvote") {
          $("#downvote-btn-" + ans_id).addClass("svg-accent-d");
          $("#downvote-value-" + ans_id).addClass("text-accent");
          var val = parseInt($("#downvote-value-" + ans_id).text());
          $("#downvote-value-" + ans_id).text((val + 1).toString());
        } else if (data == "removed_upvote_and_added_downvote") {
          $("#downvote-btn-" + ans_id).addClass("svg-accent-d");
          $("#downvote-value-" + ans_id).addClass("text-accent");
          var val = parseInt($("#downvote-value-" + ans_id).text());
          $("#downvote-value-" + ans_id).text((val + 1).toString());
          $("#upvote-btn-" + ans_id).removeClass("svg-accent-u");
          $("#upvote-value-" + ans_id).removeClass("text-accent");
          var val = parseInt($("#upvote-value-" + ans_id).text());
          $("#upvote-value-" + ans_id).text((val - 1).toString());
        } else if (data == "removed_downvote") {
          $("#downvote-btn-" + ans_id).removeClass("svg-accent-d");
          $("#downvote-value-" + ans_id).removeClass("text-accent");
          var val = parseInt($("#downvote-value-" + ans_id).text());
          $("#downvote-value-" + ans_id).text((val - 1).toString());
        }
      },
      error: function (data) {
        alert(data);
      },
    });
  });
}
for (var i = 0; i < accept_btns.length; i++){
  accept_btns[i].addEventListener("click", function() {
    var ans_id,ques_id;
    ans_id = $(this).attr("data-answer-id");
    ques_id = $(this).attr("data-question-id");
    $.ajax({
      type: "GET",
      url: "/faq/accept-answer/",
      data: {
        answer_id: ans_id,
        question_id: ques_id,
      },
      success: function (data) {
        if (data == "accepted_answer"){
          window.location.reload();
        } else {
          alert(data);
        }
      }
    })
  })
}



