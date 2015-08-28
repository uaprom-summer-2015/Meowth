(function (factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module.
    define(['npm-zepto'], factory);
  } else if (typeof module === 'object' && module.exports) {
    // Node/CommonJS
    module.exports = factory(require('npm-zepto'));
  } else {
    // Browser globals
    factory($);
  }
}(function ($) {

  "use strict";


}));
