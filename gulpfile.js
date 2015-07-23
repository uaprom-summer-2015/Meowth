var gulp = require('gulp');
var config = require('./gulp.conf.json')

var del = require('del')

gulp.task('build', ['build:scripts'])

gulp.task('build:scripts', function() {
  // TODO: provide code
});

gulp.task('clean', function(cb) {
  glob = config.dist + '/*';
  return del([glob, '!.gitignore'], function(err, paths) {
    console.log('Deleted files/folders:\n', paths.join('\n'));
  });
});
