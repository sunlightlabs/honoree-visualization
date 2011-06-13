$(function() {
    // states
    var states = {AL:"Alabama",AK:"Alaska",AZ:"Arizona",AR:"Arkansas",CA:"California",CO:"Colorado",CT:"Connecticut",DE:"Delaware",DC:"District of Columbia",FL:"Florida",GA:"Georgia",GU:"Guam",HI:"Hawaii",ID:"Idaho",IL:"Illinois",IN:"Indiana",IA:"Iowa",KS:"Kansas",KY:"Kentucky",LA:"Louisiana",ME:"Maine",MD:"Maryland",MA:"Massachusetts",MI:"Michigan",MN:"Minnesota",MS:"Mississippi",MO:"Missouri",MT:"Montana",NE:"Nebraska",NV:"Nevada",NH:"New Hampshire",NJ:"New Jersey",NM:"New Mexico",NY:"New York",NC:"North Carolina",ND:"North Dakota",OH:"Ohio",OK:"Oklahoma",OR:"Oregon",PA:"Pennsylvania",RI:"Rhode Island",SC:"South Carolina",SD:"South Dakota",TN:"Tennessee",TX:"Texas",UT:"Utah",VT:"Vermont",VA:"Virginia",WA:"Washington",WV:"West Virginia",WI:"Wisconsin",WY:"Wyoming"};
    
    // Microtemplates, swiped from underscore
    var _ = {};
    _.templateSettings = {
        evaluate    : /<%([\s\S]+?)%>/g,
        interpolate : /<%=([\s\S]+?)%>/g
    };
    
    _.template = function(str, data) {
        var c  = _.templateSettings;
        var tmpl = 'var __p=[],print=function(){__p.push.apply(__p,arguments);};' +
            'with(obj||{}){__p.push(\'' +
            str.replace(/\\/g, '\\\\')
               .replace(/'/g, "\\'")
               .replace(c.interpolate, function(match, code) {
                   return "'," + code.replace(/\\'/g, "'") + ",'";
               })
               .replace(c.evaluate || null, function(match, code) {
                   return "');" + code.replace(/\\'/g, "'")
                                      .replace(/[\r\n\t]/g, ' ') + "__p.push('";
               })
               .replace(/\r/g, '\\r')
               .replace(/\n/g, '\\n')
               .replace(/\t/g, '\\t')
               + "');}return __p.join('');";
        var func = new Function('obj', tmpl);
        return data ? func(data) : func;
    };
    
    // template formatting stuff
    var template_helpers = {
        'formatDollars': function(number) {
            var out = [], counter = 0, part = true;
            var digits = number.toFixed(0).split("");
            while (part) {
                part = (counter == 0 ? digits.slice(-3) : digits.slice(counter - 3, counter)).join("");
                if (part) {
                    out.unshift(part);
                    counter -= 3;
                }
            }
            return out.join(",");
        },
        'formatDate': function(date) {
            var d = new Date(date);
            return [
                ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][d.getMonth()],
                ' ',
                d.getDate(),
                ', ',
                d.getFullYear()
            ].join("");
        }
    }
    
    // actual templates
    var templates = {
        main_row: _.template("{% filter escapejs %}{% spaceless %}{% include 'honorees/main_row.mt.html' %}{% endspaceless %}{% endfilter %}"),
        dropdown_honoree: _.template("{% filter escapejs %}{% spaceless %}{% include 'honorees/dropdown_honoree.mt.html' %}{% endspaceless %}{% endfilter %}"),
        dropdown_registrant: _.template("{% filter escapejs %}{% spaceless %}{% include 'honorees/dropdown_registrant.mt.html' %}{% endspaceless %}{% endfilter %}")
    }
    
    // select the right thing
    $('.view-by[value=honoree]').attr('checked', true);
    
    //utility functions
    var updateTitle = function(type, title, table) {
        var count = table.find('li:visible').length;
        title.html(type.charAt(0).toUpperCase() + type.slice(1) + " <span class='tip'>" + (count == 0 ? "" : "(" + template_helpers.formatDollars(count) + " Total)") + "</span>")
    }
    
    // events
    $('.view-by').change(function() {
        var toShow = $('input[name=view-by]:checked').val();
        var table = $('ol#' + toShow + '-table');
        
        if (table.children().length == 0) {
            table.addClass('loading');
            $.getJSON('all_' + toShow + 's.json', function(data) {
                var most = data[0].total_contributions;
                table.removeClass('loading');
                $.each(data, function(idx, row) {
                    table.append(templates.main_row($.extend({'most': most, 'type': toShow}, template_helpers, row)));
                })
                
                updateTitle(toShow, $('#honoreeTitle'), table);
            });
        }
        
        $('ol').not('#' + toShow + '-table').hide();
        table.show();
        
        $('.filterDropdown').hide();
        
        updateTitle(toShow, $('#honoreeTitle'), table);
        
        // clear filter
        $('.filterDropdown').find('input.checkbox').attr('checked', true).end().find('input[name="word"]').val('').end().find('input[name="state"]').val('');
        
        //show everything
        table.find('li').show();
    })
    
    $('#container').delegate('.mainAmountTable li .clickable', 'click', function() {
        var $this = $(this);
        var $parent = $this.parent();
        if ($parent.hasClass('active')) {
            $parent.removeClass('active');
            $parent.find('.dropdownTable').hide();
        } else {
            $parent.addClass('active');
            var $dropdown = $parent.find('.dropdownTable');
            if ($dropdown.children().length == 0) {
                $dropdown.addClass('loading');
                
                var type = $parent.data('db-type');
                var id = $parent.data('db-id');
                $.getJSON(type + '/' + id + '.json', function(data) {
                    $dropdown.removeClass('loading');
                    
                    $dropdown.html(templates['dropdown_' + type]($.extend({'data': data}, template_helpers)));
                })
            }
            $dropdown.slideDown('fast');
        }
        return false;
    });
    
    $('#filterBtn').click(function() {
        var showing = $('input[name=view-by]:checked').val();
        $('#' + showing + 'Filter').slideToggle('fast');
        return false;
    })
    
    var applyNameFilter = function(type, original) {
        var query = original.toLowerCase();
        $('#' + type + '-table span.honoreeName').each(function(idx, element) {
            var $element = $(element);
            if ($element.html().toLowerCase().indexOf(query) == -1) {
                $element.parents('li').hide();
            }
        })
    }
    
    $('#honoreeFilter').find('input.checkbox').change(function() {
        var $this = $(this);
        if ($this.attr('checked')) {
            if ($this.attr('name') == 'all') {
                $('#honoreeFilter input.checkbox').attr('checked', true);
            }
        } else {
            if ($this.attr('name') != 'all') {
                $('#honoreeFilter input.checkbox[name="all"]').attr('checked', false);
            }
        }
    }).end().find('button.btnFilter').click(function() {
        // hide everything
        $('#honoree-table li').hide();
        
        // find category matches
        var state_selector = [];
        $('#honoreeFilter input.checkbox:checked').each(function(idx, val) {
            if (val != "all") {
                state_selector.push('#honoree-table li.category-' + $(val).attr('name'));
            }
        });
        
        var set = $(state_selector.join(','));
        
        var state = $('#honoreeFilter select[name="state"]').val();
        if (state) {
            set = set.filter('li.state-' + state);
        }
        
        set.show();
        
        var nameQuery = $('#honoreeFilter input[name="word"]').val();
        if (nameQuery) {
            applyNameFilter('honoree', nameQuery);
        }
        
        updateTitle('honoree', $('#honoreeTitle'), $('#honoree-table'));
        
        $('#honoreeFilter').slideUp('fast');
    })
    
    $('#registrantFilter button.btnFilter').click(function() {
        $('#registrant-table li').show();
        
        var nameQuery = $('#registrantFilter input[name="word"]').val();
        if (nameQuery) {
            applyNameFilter('registrant', nameQuery);
        }
        
        updateTitle('registrant', $('#honoreeTitle'), $('#registrant-table'));
        
        $('#registrantFilter').slideUp('fast');
    })
    
    // populate state dropdown
    var stateFilter = $('#honoreeFilter select[name="state"]');
    $.each(states, function(key, value) {
        stateFilter.append('<option value="' + key + '">' + value + '</option>');
    })
    
    $('.view-by').eq(0).change();
})