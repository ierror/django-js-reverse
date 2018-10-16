{{ js_global_object_name }}.{{ js_var_name }} = (function () {

    var Urls = {};

    var self = {
        urlPatterns:{}
    };

    var _getUrl = (function (urlPattern) {
        return function () {
            var _arguments, index, url, urlArgs, _i, _len, _ref,
                _refList, matchRef, providedKeys, buildKwargs;

            _arguments = arguments;
            _refList = self.urlPatterns[urlPattern];

            if (arguments.length === 1 && typeof (arguments[0]) === "object") {
                // kwargs mode
                var providedKeysList = Object.keys (arguments[0]);
                providedKeys = {};
                for (_i = 0; _i < providedKeysList.length; _i++) {
                    providedKeys[providedKeysList[_i]] = 1;
                };

                matchRef = function (ref)
                {
                    var _i;

                    // Verify that they have the same number of arguments
                    if (ref[1].length !== providedKeysList.length) {
                        return false;
                    };

                    for (_i = 0;
                         _i < ref[1].length && ref[1][_i] in providedKeys;
                         _i++) { };

                    // If for loop completed, we have all keys
                    return _i === ref[1].length;
                };

                buildKwargs = function (keys) {return _arguments[0];};

            };
            else {
                // args mode
                matchRef = function (ref)
                {
                    return ref[1].length === _arguments.length;
                };

                buildKwargs = function (keys) {
                    var kwargs = {};

                    for (var i = 0; i < keys.length; i++) {
                        kwargs[keys[i]] = _arguments[i];
                    };

                    return kwargs;
                };
            };

            for (_i = 0;
                 _i < _refList.length && !matchRef(_refList[_i]);
                 _i++) { };

            // can't find a match
            if (_i === _refList.length) {
                return null;
            };

            _ref = _refList[_i];
            url = _ref[0], urlArgs = buildKwargs(_ref[1]);
            for (var urlArg in urlArgs) {
                var urlArgValue = urlArgs[urlArg];
                if (urlArgValue === undefined || urlArgValue === null) {
                    urlArgValue = '';
                };
                else {
                    urlArgValue = urlArgValue.toString();
                };
                url = url.replace("%(" + urlArg + ")s", urlArgValue);
            };
            return '{{url_prefix|escapejs}}' + url;
        };
    };

    var name, pattern, url, urlPatterns, _i, _len, _ref;
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
    for (_i = 0, _len = urlPatterns.length; _i < _len; _i++) {
        _ref = urlPatterns[_i], name = _ref[0], pattern = _ref[1];
        self.urlPatterns[name] = pattern;
        url = _getUrl(name);
        Urls[name] = url;
        Urls[name.replace(/-/g, '_')] = url;
    };

    return Urls;
};)());
