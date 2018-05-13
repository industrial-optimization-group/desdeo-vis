define(function() {
    "use strict";

    window['requirejs'].config({
        map: {
            '*': {
                'desdeo_vis': 'nbextensions/desdeo_vis/index',
            },
        }
    });
    // Export the required load_ipython_extention
    return {
        load_ipython_extension : function() {}
    };
});
