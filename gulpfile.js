var gulp = require('gulp');
var pkginfo = require('./package.json');

var browserify = require('browserify');
var buffer = require('vinyl-buffer');
var del = require('del');
var gutil = require('gulp-util');
var rename = require('gulp-rename');
var source = require('vinyl-source-stream');
var stylus = require('gulp-stylus');
var uglify = require('gulp-uglify');



gulp.task('build', ['build:scripts', 'build:styles']);


gulp.task('build:scripts', function() {
  browserify({
    entries: pkginfo.assets.scripts.entries,
    paths: pkginfo.assets.scripts.paths
  }).bundle()
  .pipe(source('bundle.js'))
  .pipe(buffer())
  .pipe(gutil.env.type === 'production' ? uglify() : gutil.noop())
  .pipe(gulp.dest(pkginfo.dist));
});


gulp.task('build:styles', function() {
  gulp.src(pkginfo.assets.styles.entries).pipe(stylus({
    compress: true,
    'include css': true,
    include: pkginfo.stylus.includes
  }))
  .pipe(rename('bundle.css'))
  .pipe(gulp.dest(pkginfo.dist));
});


gulp.task('watch', ['build'], function() {
  gulp.watch(pkginfo.assets.scripts.watches, ['build:scripts']);
  gulp.watch(pkginfo.assets.styles.watches, ['build:styles']);
});


gulp.task('clean', function(callback) {
  glob = pkginfo.dist + '/*';
  del([glob, '!.gitignore'], callback);
});

gulp.task('browserify', function(){
  return browserify(pkginfo.form.file)
        .bundle()
        .pipe(source(pkginfo.form.name))
        .pipe(gulp.dest(pkginfo.dist));
});
