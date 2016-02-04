$(function(){
    var div_id = 'random_note_widget';
    var div_id_for_$ = '#' + div_id;
    if (!$(div_id_for_$).length) {
        var div = document.createElement('div');
        div.id = 'random_note_widget';
        $('body').append(div);
    }
    $.ajax({
        url: 'http://nameless-citadel-98707.herokuapp.com/random',
        dataType: 'json',
        success: function(data){
            console.log(data);
            if (data['result'] == 'success'){
                $(div_id_for_$).append(data['random_note']);
            } else {
                $(div_id_for_$).append(data['msg']);
            }
        }
    });
});