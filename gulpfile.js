var gulp = require('gulp');
var pkginfo = require('./package.json')

var browserify = require('browserify')
var buffer = require('vinyl-buffer');
var del = require('del')
var gutil = require('gulp-util');
var rename = require('gulp-rename');
var source = require('vinyl-source-stream');
var uglify = require('gulp-uglify');



gulp.task('build', ['build:scripts'])


gulp.task('build:scripts', function() {
  return browserify({
    entries: pkginfo.assets.scripts.entries,
    paths: pkginfo.assets.scripts.paths
  }).bundle()
  .pipe(source('bundle.js'))
  .pipe(buffer())
  .pipe(gutil.env.type === 'production' ? uglify() : gutil.noop())
  .pipe(gulp.dest(pkginfo.dist));
});


gulp.task('watch', ['build'], function() {
  gulp.watch(pkginfo.assets.scripts.watches, ['build:scripts']);
});


gulp.task('clean', function(callback) {
  glob = pkginfo.dist + '/*';
  return del([glob, '!.gitignore'], callback);
});
