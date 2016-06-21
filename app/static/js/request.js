/**
 * Created by garyzhou on 6/21/16.
 */
$(document).ready(function() {
    //toggle `popup` / `inline` mode
    $.fn.editable.defaults.mode = 'inline';

    //make username editable
    $('#division').editable({
        type: 'select',
        title: 'Select Divison',
        placement: 'right',
        source: $.get({
                "http://localhost:5000/divisions"
            }).done( function(data) { return JSON.parse(data); });
        ]
    })

    //make status editable
    //$('#status').editable({
    //    type: 'select',
    //    title: 'Select status',
    //    placement: 'right',
    //    value: 2,
    //    source: [
    //        {value: 1, text: 'status 1'},
    //        {value: 2, text: 'status 2'},
    //        {value: 3, text: 'status 3'}
    //    ]
    //    /*
    //    //uncomment these lines to send data on server
    //    ,pk: 1
    //    ,url: '/post'
    //    */
    //});
});

function process_divisions(data) {
    return JSON.parse(data)
}