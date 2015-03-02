{{ js_global_object_name }}.{{ js_var_name }} = (function () {

    var Urls = {};

    var self = {
        url_patterns:{}
    };

    var _get_url = function (url_pattern) {
        return function () {
            var index, url, url_arg, url_args, _i, _len, _ref, _ref_list;
            _ref_list = self.url_patterns[url_pattern];
            for (_i = 0;
                 _ref = _ref_list[_i], _ref[1].length != arguments.length;
                 _i++);

            url = _ref[0], url_args = _ref[1];
            for (index = _i = 0, _len = url_args.length; _i < _len; index = ++_i) {
                url_arg = url_args[index];
                url = url.replace("%(" + url_arg + ")s", arguments[index] || '');
            }
            return '{{url_prefix|escapejs}}' + url;
        };
    };

    var name, pattern, self, url_patterns, _i, _len, _ref;
    url_patterns = [
        {% for name, patterns in urls %}
            [
                '{{name|escapejs}}',
                [
                    {% for path, args in patterns %}
                    [
                        '{{path|escapejs}}',
                        [
                            {% for arg in args %}
                            '{{arg|escapejs}}',
                            {% endfor %}
                        ]{% if not forloop.last %},{% endif %}
                    ]{% if not forloop.last %},{% endif %}
                    {% endfor %}
                ]{% if not forloop.last %},{% endif %}
            ]{% if not forloop.last %},{% endif %}
        {% endfor %}
    ];
    self.url_patterns = {};
    for (_i = 0, _len = url_patterns.length; _i < _len; _i++) {
        _ref = url_patterns[_i], name = _ref[0], pattern = _ref[1];
        self.url_patterns[name] = pattern;
        Urls[name] = _get_url(name);
        Urls[name.replace(/-/g, '_')] = _get_url(name);
    }

    return Urls;
})();
