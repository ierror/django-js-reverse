{{ js_global_object_name }}.{{ js_var_name }} = (function () {
    var Urls = {};
    var self = {
        urlPatterns:{}
    };

    var _getUrl = function (urlPattern) {
        return function () {
            var _arguments, index, url, urlArg, urlArgs, i, _len, _ref,
                _refList, matchRef, providedKeys, build_kwargs;
            _arguments = arguments;
            _refList = self.urlPatterns[urlPattern];
            if (arguments.length === 1 && typeof (arguments[0]) === "object") {
                // kwargs mode
                var providedKeysList = Object.keys (arguments[0]);
                providedKeys = {};
                for (var i = 0; i < providedKeysList.length; i++) {
                    providedKeys[providedKeysList[i]] = 1;
                }

                matchRef = function (ref)
                {
                    var j;
                    // Verify that they have the same number of arguments
                    if (ref[1].length !== providedKeysList.length) {
                        return false;
                    }
                    for (j = 0;
                         j < ref[1].length && ref[1][j] in providedKeys;
                         j++) { ; }
                    // If for loop completed, we have all keys
                    return j === ref[1].length;
                }

                build_kwargs = function (keys) {return _arguments[0];}

            } else {
                // args mode
                matchRef = function (ref)
                {
                    return ref[1].length === _arguments.length;
                }

                build_kwargs = function (keys) {
                    var kwargs = {};

                    for (var j = 0; j < keys.length; j++) {
                        kwargs[keys[j]] = _arguments[j];
                    }

                    return kwargs;
                }
            }

            for (i = 0;
                 i < _refList.length && !matchRef(_refList[i]);
                 i++) { ; }

            // can't find a match
            if (i === _refList.length)
                return null;

            _ref = _refList[i];
            url = _ref[0], urlArgs = build_kwargs(_ref[1]);
            for (urlArg in urlArgs) {
            	var urlArgValue = urlArgs[urlArg];
            	if (urlArgValue === undefined || urlArgValue === null) {
            		urlArgValue = '';
            	} else {
            		urlArgValue = urlArgValue.toString();
            	}
                url = url.replace("%(" + urlArg + ")s", urlArgValue);
            }
            return '{{url_prefix|escapejs}}' + url;
        };
    };

    var name, pattern, url, urlPatterns, i, _len, _ref;
    urlPatterns = [
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

    self.urlPatterns = {};
    for (i = 0, _len = urlPatterns.length; i < _len; i++) {
        _ref = urlPatterns[i], name = _ref[0], pattern = _ref[1];
        self.urlPatterns[name] = pattern;
        url = _getUrl(name);
        Urls[name] = url;
        Urls[name.replace(/-/g, '_')] = url;
    }

    return Urls;
})();