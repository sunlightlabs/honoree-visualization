$(function() {
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
    
    // events
    $('.view-by').change(function() {
        var toShow = $('input[name=view-by]:checked').val();
        var table = $('ol#' + toShow + '-table');
        
        if (table.children().length == 0) {
            table.addClass('loading');
            $.getJSON('/all_' + toShow + 's.json', function(data) {
                var most = data[0].total_contributions;
                table.removeClass('loading');
                $.each(data, function(idx, row) {
                    table.append(templates.main_row($.extend({'most': most}, template_helpers, row)));
                })
                
            });
        }
        
        $('ol').not('#' + toShow + '-table').hide();
        table.show();
    })
})