require('!!file?name=[path][name].[ext]!./ckeditor/config.js');
require('!!file?name=[path][name].[ext]!./ckeditor/styles.js');
require('!!file?name=[path][name].[ext]!./ckeditor/contents.css');
require('!!file?name=[path][name].[ext]!./ckeditor/lang/en.js');
require('!!file?name=[path][name].[ext]!./ckeditor/plugins/icons.png');
require('!!file?name=[path][name].[ext]!./ckeditor/skins/moono/editor_gecko.css');
require('!!file?name=[path][name].[ext]!./ckeditor/skins/moono/icons.png');

module.exports = require('!!exports?CKEDITOR!./ckeditor/ckeditor.js');
