let upvote_btns = document.getElementsByClassName("upvote-btn");
let downvote_btns = document.getElementsByClassName("downvote-btn");

$(document).ready(function () {
    load_details();
  });
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
          $("#upvote-btn-" + ans_id).addClass("svg-accent");
          $("#upvote-value-" + ans_id).addClass("text-accent");
          var val = parseInt($("#upvote-value-" + ans_id).text());
          $("#upvote-value-" + ans_id).text((val + 1).toString());
        } else if (data == "removed_downvote_and_added_upvote") {
          $("#upvote-btn-" + ans_id).removeClass("svg-accent");
          $("#upvote-value-" + ans_id).removeClass("text-accent");
          var val = parseInt($("#upvote-value-" + ans_id).text());
          $("#upvote-value-" + ans_id).text((val + 1).toString());
          $("#downvote-btn-" + ans_id).removeClass("svg-accent");
          $("#downvote-value-" + ans_id).removeClass("text-accent");
          var val = parseInt($("#downvote-value-" + ans_id).text());
          $("#downvote-value-" + ans_id).text((val - 1).toString());
        } else if (data == "removed_upvote") {
          $("#upvote-btn-" + ans_id).removeClass("svg-accent");
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
          $("#downvote-btn-" + ans_id).addClass("svg-accent");
          $("#downvote-value-" + ans_id).addClass("text-accent");
          var val = parseInt($("#downvote-value-" + ans_id).text());
          $("#downvote-value-" + ans_id).text((val + 1).toString());
        } else if (data == "removed_upvote_and_added_downvote") {
          $("#downvote-btn-" + ans_id).addClass("svg-accent");
          $("#downvote-value-" + ans_id).addClass("text-accent");
          var val = parseInt($("#downvote-value-" + ans_id).text());
          $("#downvote-value-" + ans_id).text((val + 1).toString());
          $("#upvote-btn-" + ans_id).removeClass("svg-accent");
          $("#upvote-value-" + ans_id).removeClass("text-accent");
          var val = parseInt($("#upvote-value-" + ans_id).text());
          $("#upvote-value-" + ans_id).text((val - 1).toString());
        } else if (data == "removed_downvote") {
          $("#downvote-btn-" + ans_id).removeClass("svg-accent");
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
let load_details = function(){
    for (var i = 0; i < downvote_btns.length; i++) {
        var ans_id;
        ans_id = downvote_btns[i].getAttribute("data-answer-id");
        $.ajax({
          type: "GET",
          url: "/faq/is_downvoted/"+ans_id,
          success: function (data) {
              console.log(data);
            if (data == "downvoted") {
              $("#downvote-btn-" + ans_id).addClass("svg-accent");
              $("#downvote-value-" + ans_id).addClass("text-accent");
            }
          },
          error: function (data) {
            console.log(data);
          },
        });
      }
      for (var i = 0; i < upvote_btns.length; i++) {
        var ans_id;
        ans_id = upvote_btns[i].getAttribute("data-answer-id");
        $.ajax({
          type: "GET",
          url: "/faq/is_upvoted/"+ans_id,
          success: function (data) {
            console.log(data);
            if (data == "upvoted") {
              $("#upvote-btn-" + ans_id).addClass("svg-accent");
              $("#upvote-value-" + ans_id).addClass("text-accent");
            }
          },
          error: function (data) {
            console.log(data);
          },
        });
      }
}


