{{ js_global_object_name }}.{{ js_var_name }} = (function () {

    var Urls = {};

    var self = {
        url_patterns:{}
    };

    var _get_url = function (url_pattern) {
        return function () {
            var _arguments, index, url, url_arg, url_args, _i, _len, _ref,
                _ref_list, match_ref, provided_keys, build_kwargs;

            _arguments = arguments;
            _ref_list = self.url_patterns[url_pattern];

            if (arguments.length == 1 && typeof (arguments[0]) == "object") {
                // kwargs mode
                var provided_keys_list = Object.keys (arguments[0]);
                provided_keys = {};
                for (_i = 0; _i < provided_keys_list.length; _i++)
                    provided_keys[provided_keys_list[_i]] = 1;

                match_ref = function (ref)
                {
                    var _i;

                    // Verify that they have the same number of arguments
                    if (ref[1].length != provided_keys_list.length)
                        return false;

                    for (_i = 0;
                         _i < ref[1].length && ref[1][_i] in provided_keys;
                         _i++);

                    // If for loop completed, we have all keys
                    return _i == ref[1].length;
                }

                build_kwargs = function (keys) {return _arguments[0];}

            } else {
                // args mode
                match_ref = function (ref)
                {
                    return ref[1].length == _arguments.length;
                }

                build_kwargs = function (keys) {
                    var kwargs = {};

                    for (var i = 0; i < keys.length; i++) {
                        kwargs[keys[i]] = _arguments[i];
                    }

                    return kwargs;
                }
            }

            for (_i = 0;
                 _i < _ref_list.length && !match_ref(_ref_list[_i]);
                 _i++);

            // can't find a match
            if (_i == _ref_list.length)
                return null;

            _ref = _ref_list[_i];
            url = _ref[0], url_args = build_kwargs(_ref[1]);
            for (url_arg in url_args) {
            	var url_arg_value = url_args[url_arg];
            	if (url_arg_value === undefined || url_arg_value === null) {
            		url_arg_value = '';
            	} else {
            		url_arg_value = url_arg_value.toString();
            	}
                url = url.replace("%(" + url_arg + ")s", url_arg_value);
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
