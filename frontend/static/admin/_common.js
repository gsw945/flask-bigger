/**
 * 获取地址栏参数值
 * @param param_key 地址栏参数键名
 */
function getUrlParam(param_key) {
    var arr = window.location.search.replace(/^[\?]/, '').split('&');
    for (var i = 0; i < arr.length; i++) {
        var value = arr[i].replace(/^[^\=]+[\=]/, '');
        if(arr[i].replace(value, '') == param_key + '=') {
            return value;
        }
    }
    return null;
}

/**
 * 时间戳转字符串时间(YYYY-MM-dd HH:mm:ss)
 * @param timestamp 时间戳(单位秒)
 */
function ts2str(timestamp) {
    var padLeftZero = function(num) {
        return [(num <= 9) ? '0' : '', num].join('');
    };
    timestamp = Number(timestamp) * 1000;
    var dt = new Date(timestamp);
    return [
        dt.getFullYear(),
        padLeftZero(dt.getMonth() + 1),
        padLeftZero(dt.getDate())
    ].join('-') + ' ' +
    [
        padLeftZero(dt.getHours()),
        padLeftZero(dt.getMinutes()),
        padLeftZero(dt.getSeconds())
    ].join(':');
}

function get_hm_min(hm) {
    var hm_min = new Date(hm.setHours(0));
    hm_min = new Date(hm_min.setMinutes(0));
    return new Date(hm_min.setSeconds(0));
}
function get_hm_max(hm) {
    var hm_max = new Date(hm.setHours(23));
    hm_max = new Date(hm_max.setMinutes(59));
    return new Date(hm_max.setSeconds(59));
}
function default_min_date(now) {
    if(!now) {
        now = new Date();
    }
    var now_1 = new Date(now.getTime() - 1000 * 3600 * 24 * 1);
    // 06:00:00
    now_1 = new Date(now_1.setHours(6));
    now_1 = new Date(now_1.setMinutes(0));
    return new Date(now_1.setSeconds(0));
}
function default_max_date(now) {
    if(!now) {
        now = new Date();
    }
    var now_0 = new Date(now.getTime());
    // 05:59:59
    now_0 = new Date(now_0.setHours(5));
    now_0 = new Date(now_0.setMinutes(59));
    return new Date(now_0.setSeconds(59));
}

// 获取datepicker配置
function get_dp_cfg(format, min_date, max_date) {
    // refer: datepicker-doc( http://t1m0n.name/air-datepicker/docs/ )
    // console.log(format);
    var _cfg = {};
    var now = new Date(), // 当前时间
        d_ms = 3600 * 24 * 1000; // 一天的毫秒数
    var y_1st = new Date(new Date().setMonth(0)); // 1月
    var m_start = new Date(y_1st.setDate(1)), // 1月第一天
        m_end = new Date(y_1st.setDate(28)); // 1月最后一天(通用,包括平年2月)

    switch(format) {
        case '%Y-%m-%d %H:%M':
            _cfg = {
                dateFormat: 'yyyy-mm-dd',
                timepicker: true,
                timeFormat: 'hh:ii'
            };
            /*
            if(min_date) {
                if((typeof min_date == 'number') && min_date > 0) {
                    _cfg['minDate'] = new Date(now.getTime() + d_ms * min_date);
                }
                else if(min_date instanceof Date) {
                    _cfg['minDate'] = min_date;
                }
            }
            if(!_cfg['minDate']) {
                _cfg['minDate'] = default_min_date();
            }
            if(max_date) {
                alert(max_date)
                if((typeof max_date == 'number') && max_date > 0) {
                    _cfg['maxDate'] = new Date(now.getTime() + d_ms * max_date);
                }
                else if(max_date instanceof Date) {
                    _cfg['maxDate'] = max_date;
                }
            }
            */
            break;
        case '%H:%M':
            _cfg = {
                navTitles: {
                    years: '<h3>选择时间</h3>'
                },
                view: 'years',
                minView: 'years',
                dateFormat: ' ',
                dateTimeSeparator: '',
                onSelect: function(formattedDate, date, inst) {
                    inst.$el.val(formattedDate.trim());
                },
                minDate: get_hm_min(now),
                maxDate: get_hm_max(now),
                classes: 'hide-date-part',
                timepicker: true,
                timeFormat: 'hh:ii'
            };
            break;
        case '%d %H:%M':
            _cfg = {
                navTitles: {
                    days: '<h3>选择时间点</h3>'
                },
                startDate: m_end,
                minDate: m_start,
                maxDate: m_end,
                onShow: function(inst, animationCompleted) {
                    inst.$nav.off('click');
                    var $weeks = inst.$content.find('.datepicker--days.datepicker--body');
                    $weeks.find('.datepicker--days-names').hide();
                },
                view: 'days',
                minView: 'days',
                dateFormat: 'dd',
                timepicker: true,
                timeFormat: 'hh:ii'
            };
            break;
        case '%Y-%m-%d':
            break;
        case '%Y-%m':
            _cfg = {
                dateFormat: 'yyyy-mm',
                view: 'months',
                minView: 'months',
                minDate: new Date(now.getTime() - d_ms * 365), // 历史数据,最多支持计算一年以内的
                maxDate: now
            };
            break;
        case '%Y':
            _cfg = {
                navTitles: {
                    years: '<h3>选择年份</h3>'
                },
                dateFormat: 'yyyy',
                view: 'years',
                minView: 'years',
                minDate: new Date(now.getTime() - d_ms * 365),
                maxDate: now
            };
            break;
        case '%Y ~ %Y':
            _cfg = {
                range: true,
                multipleDatesSeparator: ' ~ ',
                dateFormat: 'yyyy',
                view: 'years',
                minView: 'years',
                minDate: new Date(now.getTime() - d_ms * 365), // 历史数据,最多支持计算一年以内的
                maxDate: now
            };
            break;
        case '%Y-%m-%d ~ %Y-%m-%d':
            _cfg = {
                range: true,
                multipleDatesSeparator: ' ~ ',
                dateFormat: 'yyyy-mm-dd',
                view: 'days',
                minView: 'days',
                minDate: new Date(now.getTime() - d_ms * 365), // 历史数据,最多支持计算一年以内的
                maxDate: now
            };
            break;
        case '%Y-%m ~ %Y-%m':
            _cfg = {
                range: true,
                multipleDatesSeparator: ' ~ ',
                dateFormat: 'yyyy-mm',
                view: 'months',
                minView: 'months',
                minDate: new Date(now.getTime() - d_ms * 365), // 历史数据,最多支持计算一年以内的
                maxDate: now
            };
            break;
        default:
            break;
    }
    _cfg['onSelect'] = function(formattedDate, date, inst) {
        var $input = inst.$el;
        setTimeout(function() {
            $input.trigger('change');
        }, 80);
    };
    return _cfg;
}

function add_datepicker(format, $elem, min_date, max_date) {
    var old_dp = $elem.data('datepicker');
    if(old_dp) {
        old_dp.destroy();
    }
    var default_cfg = {
        language: 'zh',
        toggleSelected: false,
        autoClose: true,
        firstDay: 0
    };
    var _dp_cfg = get_dp_cfg(format, min_date, max_date);
    var _cfg = $.extend({}, default_cfg, _dp_cfg, true);
    $elem.datepicker(_cfg);
}