$(function() {
    var index = 0;
    var play = null;
    $('.little li').hover(function() {
        clearInterval(play);
        index = $(this).index();
        $(this).addClass('active').siblings().removeClass('active');
        $('.ban-main li').eq(index).show().siblings().hide();
    }, function() {
        console.log(index);
        // index = $(this).index();
        autoplay(index);
    });
    $('.list-nav li').bind('click',function () {
        $(this).addClass('active').siblings().removeClass('active');
    });
    // $('#jsStayBtn').on('click', function () {
    //     $.ajax({
    //         type: 'POST',
    //         url: "{% url 'org:add_ask' %}",
    //         data: $('#jsStayForm').serialize(),
    //         async: true,
    //         success: function (data) {
    //             console.log(data);
    //             if(data.status == 'success'){
    //                 $('#jsStayForm')[0].reset();
    //                 console.log('提交成功');
    //             }else if(data.status == 'fail'){
    //                 console.log(data.msg);
    //                 console.log('提交失败');
    //             }
    //         }
    //     })
    // })

    function autoplay(num) {
        play = setInterval(function(num) {
            index = (num != undefined) ? num : ++index;
            index = (index > 3) ? 0 : index;
            $('.little li').eq(index).addClass('active').siblings().removeClass('active');
            $('.ban-main li').eq(index).show().siblings().hide();

        }, 2000);
    }
    autoplay();
});

