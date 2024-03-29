$(document).ready(function () {

    ////////////////////////////////////////
    // Mutation observer - watch for RTL
    ////////////////////////////////////////

    var target = document.querySelector('html');

    var observer = new MutationObserver( function(mutations) {
        mutations.forEach( function() {
            var classes = target.getAttribute('class');
            var single_class = 'translated-rtl';
            if (classes.includes(single_class)) {
                target.setAttribute('dir', 'rtl');
            } else {
                target.setAttribute('dir', 'ltr');
            }
        });
    });

    var config = {
        attributes: true,
        attributeFilter: ['class']
    }
    
    observer.observe(target, config);

    ////////////////////////////////////////
    // Language, Search, and Menu Toggle
    ////////////////////////////////////////

    $('#global-language').on('show.bs.collapse', function () {
        $('#global-search').collapse('hide');
        $('#nav-primary').collapse('hide');
    });

    $('#global-search').on('show.bs.collapse', function () {
        $('#global-language').collapse('hide');
        $('#nav-primary').collapse('hide');
    });

    $('#nav-primary').on('show.bs.collapse', function () {
        $('#global-search').collapse('hide');
        $('#global-language').collapse('hide');
    });

    ////////////////////////////////////////
    // Language and Search Toggle Focus
    ////////////////////////////////////////

    $('#global-language').on('shown.bs.collapse', function () {
        $('.goog-te-combo').focus();
    }).on('show.bs.collapse', function () {
        $('.goog-te-combo').blur();
    });

    $('#global-search').on('shown.bs.collapse', function () {
        document.getElementById('global-search-bar').focus();
    }).on('show.bs.collapse', function () {
        document.getElementById('global-search-bar').blur();
    });

    ////////////////////////////////////////
    // Back to top
    ////////////////////////////////////////

    var scroll_speed = 800;

    if( $('#back-to-top').length ){

        $('#back-to-top > a').click(function() {
            $('body, html').animate({
                scrollTop: 0
            }, scroll_speed );
        });

        $(window).scroll(function() {

            var window_scroll = $(document).scrollTop();
            var primary_content = $('#primary-content').offset().top;

            if ( window_scroll > primary_content ) {
                $('#back-to-top').addClass('show');
            } else {
                $('#back-to-top').removeClass('show');
            }

        }).scroll();
    }

});

////////////////////////////////////////
// Google Translate Links
////////////////////////////////////////

$('.lang-select').click(function (e) {
    e.preventDefault();
    var lang = $(this).attr('data-lang')
    setLanguage(lang);
});

function setLanguage(theLang) {
    var theSelect = $('.goog-te-combo');
    var db = theSelect.get(0);
    theSelect.val(theLang);
    fireEvent(db, 'change');
}

function fireEvent(element, event) {
    if (document.createEventObject) {
        var evt = document.createEventObject();
        return element.fireEvent('on' + event, evt)
    } else {
        var evt = document.createEvent("HTMLEvents");
        // event type, bubbling, cancelable
        evt.initEvent(event, false, true); 
        return !element.dispatchEvent(evt);
    }
}

////////////////////////////////////////
// Boostrap4 boostrap-table
////////////////////////////////////////


var $table = $('#table')
  var $remove = $('#remove')
  var selections = []

  function getIdSelections() {
    return $.map($table.bootstrapTable('getSelections'), function (row) {
      return row.id
    })
  }

  function responseHandler(res) {
    $.each(res.rows, function (i, row) {
      row.state = $.inArray(row.id, selections) !== -1
    })
    return res
  }

  function detailFormatter(index, row) {
    var html = []
    $.each(row, function (key, value) {
      html.push('<p><b>' + key + ':</b> ' + value + '</p>')
    })
    return html.join('')
  }

  function operateFormatter(value, row, index) {
    return [
      '<a class="like" href="javascript:void(0)" title="Like">',
      '<i class="fa fa-heart"></i>',
      '</a>  ',
      '<a class="remove" href="javascript:void(0)" title="Remove">',
      '<i class="fa fa-trash"></i>',
      '</a>'
    ].join('')
  }

  window.operateEvents = {
    'click .like': function (e, value, row, index) {
      alert('You click like action, row: ' + JSON.stringify(row))
    },
    'click .remove': function (e, value, row, index) {
      $table.bootstrapTable('remove', {
        field: 'id',
        values: [row.id]
      })
    }
  }

  function totalTextFormatter(data) {
    return 'Total'
  }

  function totalNameFormatter(data) {
    return data.length
  }

  function totalPriceFormatter(data) {
    var field = this.field
    return '$' + data.map(function (row) {
      return +row[field].substring(1)
    }).reduce(function (sum, i) {
      return sum + i
    }, 0)
  }

  function initTable() {
    $table.bootstrapTable('destroy').bootstrapTable({
      height: 550,
      locale: $('#locale').val(),
      columns: [
        [
          {
            field: 'state',
            checkbox: true,
            rowspan: 2,
            align: 'center',
            valign: 'middle'
          },
          {
            title: 'Item ID',
            field: 'id',
            rowspan: 2,
            align: 'center',
            valign: 'middle',
            sortable: true,
            footerFormatter: totalTextFormatter
          },
          {
            title: 'Item Detail',
            colspan: 3,
            align: 'center'
          }
        ],
        [
          {
            field: 'name',
            title: 'Item Name',
            sortable: true,
            footerFormatter: totalNameFormatter,
            align: 'center'
          },
          {
            field: 'price',
            title: 'Item Price',
            sortable: true,
            align: 'center',
            footerFormatter: totalPriceFormatter
          },
          {
            field: 'operate',
            title: 'Item Operate',
            align: 'center',
            clickToSelect: false,
            events: window.operateEvents,
            formatter: operateFormatter
          }
        ]
      ]
    })
    $table.on('check.bs.table uncheck.bs.table ' +
      'check-all.bs.table uncheck-all.bs.table',
    function () {
      $remove.prop('disabled', !$table.bootstrapTable('getSelections').length)

      // save your data, here just save the current page
      selections = getIdSelections()
      // push or splice the selections if you want to save all data selections
    })
    $table.on('all.bs.table', function (e, name, args) {
      console.log(name, args)
    })
    $remove.click(function () {
      var ids = getIdSelections()
      $table.bootstrapTable('remove', {
        field: 'id',
        values: ids
      })
      $remove.prop('disabled', true)
    })
  }

  $(function() {
//    initTable()

    $('#locale').change(initTable)
  })


 ////////////////////////////////////////
// PhoneNumber formation mask
////////////////////////////////////////
function phoneFormat(input) {//returns (###) ###-####
    input = input.replace(/\D/g,'');
    var size = input.length;
    if (size>0) {input="("+input}
    if (size>3) {input=input.slice(0,4)+") "+input.slice(4,11)}
    if (size>6) {input=input.slice(0,9)+"-" +input.slice(9)}
    return input;
}

