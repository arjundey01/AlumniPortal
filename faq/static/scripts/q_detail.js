let upvote_btns = document.getElementsByClassName('upvote-btn')
let downvote_btns = document.getElementsByClassName('downvote-btn')

for (var i = 0; i < upvote_btns.length; i++) {
    upvote_btns[i].addEventListener('click', function() {
        var ans_id,q_id;
        q_id = $(this).attr("data-question-id");
        ans_id = $(this).attr("data-answer-id");
        $.ajax({
            type: "GET",
            url: '/faq/upvote',
            data: {
                answer_id: ans_id
            },
            success: function(data) {
                console.log(data);
            }
        });
    });
 }