/**
 * Created by garyzhou on 6/21/16.
 */

/* global $ */

$(document).ready(function () {
  // toggle `popup` / `inline` mode
  $.fn.editable.defaults.mode = 'inline'

  // make division editable
  $('#division').editable({
    type: 'select',
    title: 'Select a Division',
    placement: 'right',
    source: [
      {value: 'MRMD', text: 'Records Management'},
      {value: 'ARC', text: 'Archives'},
      {value: 'GRA', text: 'Grants'},
      {value: 'LIB', text: 'Library'},
      {value: 'EXEC', text: 'Executive'},
      {value: 'MIS', text: 'MIS/Web'},
      {value: 'ADM', text: 'Administration'}
    ],
    pk: "{{ request.id }}",
    url: '/requests/edit',
    send: 'always'
  })

  // make item editable
  $('#item').editable({
    type: 'text',
    title: 'Enter Item Description',
    placement: 'right',
    pk: 2,
    url: '/requests/edit',
    send: 'always'
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
  // TODO: Funding Source Additional Info goes here.
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
})
