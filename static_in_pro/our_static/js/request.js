$(document).ready(function() {

    var title = document.title;

    function HandleVisibility(viewed) {
        console.log(viewed);
        $.ajax({
            type: 'GET',
            url: '/request-counter/',
            data: {
                'viewed': viewed
            },
            error: function(data) {
                console.log('Error (function GetData)');
                console.log(data);
            },
            success: function(data) {
                console.log(data['object_list']);
                $.each(data['object_list'], function(index, value) {
                    var li = $('.list-unstyled > li:eq(' + index + ')');
                    li.find('.obj-id').html(value['id']);
                    li.find('.obj-title').html(value['title']);
                    li.find('.obj-timestamp').html(value['timestamp']);
                    var viewed_html = viewed ? 'True' : 'False';
                    li.find('.obj-viewed').html(viewed_html);
                });
                count = data['request_counter'];
                console.log(count);
                document.title = (!viewed & count > 0) ? '(' + count + ') ' + title : title;
            }
        });
    }
    setInterval(function() {
        HandleVisibility(!Visibility.hidden());
    }, 2000);
});