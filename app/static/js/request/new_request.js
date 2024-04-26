$(document).ready(function () {
    //InputMask for phone number, tax
    $('#vendor_phone').inputmask({"mask": "(999) 999-9999"});
    $('#vendor_fax').inputmask({"mask": "(999) 999-9999"});

    //InputMask for formatting currency
    Inputmask.extendAliases({
        dollar: {
            prefix: "$ ",
            groupSeparator: ".",
            alias: "numeric",
            placeholder: "0",
            autoGroup: true,
            digits: 2,
            digitsOptional: false,
            clearMaskOnLostFocus: false,
            rightAlign: false
        }
    });
    $('#unit_price').inputmask({alias: "dollar"});
    $('#total_cost').inputmask({alias: "dollar"});


    // Handle funding source selection change
    function handleFundingSourceChange() {
        if ($('#funding_source').val() == 'Other') {
            $('#funding_source_description').show();
            $('#grant_name').hide();
            $('#project_name').hide();
        } else if ($('#funding_source').val() == 'Grant') {
            $('#grant_name').show();
            $('#project_name').show();
            $('#funding_source_description').hide();
        } else {
            $('#funding_source_description').hide();
            $('#grant_name').hide();
            $('#project_name').hide();
        }
    }

    // Initial call on page load
    handleFundingSourceChange();

    $('#funding_source').on('change', handleFundingSourceChange);

    // Retrieve vendor information on selection change
    $("#vendor_information").change(function () {
        $.ajax({
            url: "/parse_vendor",
            type: "GET",
            data: {
                vendor: $("#vendor_information").children(":selected").attr("value")
            },
            success: function (data) {
                var dis = false;
                var vendor_name = $("#vendor_name");
                var vendor_address = $("#vendor_address");
                var vendor_phone = $("#vendor_phone");
                var vendor_fax = $("#vendor_fax");
                var vendor_email = $("#vendor_email");
                var vendor_taxid = $("#vendor_taxid");
                var vendor_mwbe = $("#request_vendor_mwbe");

                if (data === "") {
                    vendor_name.val("");
                    vendor_address.val("");
                    vendor_phone.val("");
                    vendor_fax.val("");
                    vendor_email.val("");
                    vendor_taxid.val("");
                    vendor_mwbe.prop("checked", false);
                } else {
                    dis = true;
                    vendor_name.val(data[0]);
                    vendor_address.val(data[1]);
                    vendor_phone.val(data[2]);
                    vendor_fax.val(data[3]);
                    vendor_email.val(data[4]);
                    vendor_taxid.val(data[5]);
                    vendor_mwbe.prop("checked", data[6]);
                }

                vendor_name.attr("disabled", dis);
                vendor_address.attr("disabled", dis);
                vendor_phone.attr("disabled", dis);
                vendor_fax.attr("disabled", dis);
                vendor_email.attr("disabled", dis);
                vendor_taxid.attr("disabled", dis);
                vendor_mwbe.attr("disabled", dis);
            },
            error: function (error) {
                alert(error.responseJSON);
            }
        });
    });
});