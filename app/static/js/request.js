/**
 * Created by garyzhou on 6/21/16.
 */
$(document).ready(function() {
    //toggle `popup` / `inline` mode
    $.fn.editable.defaults.mode = 'inline';

    //make division editable
    $('#division').editable({
        type: 'select',
        title: 'Select Divison',
        placement: 'right',
        //source: $.getJSON({
        //        "http://localhost:5000/divisions"
        //    }).done( function(data) { return JSON.parse(data); })
    })

    $('#item').editable({
        type: 'text',
        title: 'Enter Item Description',
        placement: 'right'
    })

    $('#quantity').editable({
        type: 'text',
        title: 'Enter Quantity',
        placement: 'right'
    })

    $('#unit_price').editable({
        type: 'text',
        title: 'Enter Unit Price',
        placement: 'right'
    })

    $('#total_cost').editable({
        type: 'text',
        title: 'Enter Total Cost',
        placement: 'right'
    })

    $('#funding_source').editable({
        type: 'text',
        title: 'Enter Funding Source',
        placement: 'right'
    })
    //TODO: Funding Source Additional Info goes here.
    $('#justification').editable({
        type: 'text',
        title: 'Enter Justification',
        placement: 'right'
    })

    $('#vendor_name').editable({
        type: 'text',
        title: 'Enter Vendor Name',
        placement: 'right'
    })

    $('#vendor_address').editable({
        type: 'text',
        title: 'Enter Vendor Address',
        placement: 'right'
    })

    $('#vendor_phone').editable({
        type: 'text',
        title: 'Enter Vendor Phone',
        placement: 'right'
    })

    $('#vendor_fax').editable({
        type: 'text',
        title: 'Enter Vendor Fax',
        placement: 'right'
    })

    $('#vendor_email').editable({
        type: 'text',
        title: 'Enter Vendor Email',
        placement: 'right'
    })

    $('#vendor_taxid').editable({
        type: 'text',
        title: 'Enter Vendor Tax ID',
        placement: 'right'
    })

    $('#vendor_mwbe').editable({
        type: 'text',
        title: 'Enter M/WBE',
        placement: 'right'
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