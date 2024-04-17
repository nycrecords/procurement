$(document).ready(function(){
    //Retrieve update information
    $.ajax({
        url: 'status/' + $('#request-id').text(),
        type: 'GET',
        success: function (data){
            $('#status-history').html(data['history_rows']);
        }
    })
})