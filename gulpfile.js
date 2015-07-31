var gulp = require('gulp');
var pkginfo = require('./package.json');
var path = require('path');
var es = require('event-stream');
var glob = require('glob');
var browserify = require('browserify');
var buffer = require('vinyl-buffer');
var del = require('del');
var gutil = require('gulp-util');
var rename = require('gulp-rename');
var source = require('vinyl-source-stream');
var stylus = require('gulp-stylus');
var uglify = require('gulp-uglify');
var _ = require('lodash');
var fs = require('vinyl-fs');

var debug = gutil.env.type !== 'production';

var npmPackages = _.keys(require('./package.json').dependencies) || [];

gulp.task('default', ['build:scripts', 'build:styles']);

gulp.task('build:scripts', ['build:scripts:app', 'build:scripts:vendor']);

gulp.task('build:scripts:app', function (done) {
    glob(pkginfo.assets.scripts.entries, function (err, files) {

        if (err) done(err);
        var tasks = files.map(function (file) {
                var b = browserify({
                    debug: debug,
                    entries: [file]
                });
                npmPackages.forEach(function (id) {
                    b.external(id);
                });
                return b
                    .bundle()
                    .pipe(source(path.basename(file)))
                    .pipe(rename({
                        extname: ".bundle.js"
                    }))
                    .pipe(buffer())
                    .pipe(debug ? gutil.noop() : uglify())
                    .pipe(gulp.dest(pkginfo.dist));
        });
        es.merge(tasks).on('end', done);
    });
});

gulp.task('build:scripts:vendor', [
    "build:scripts:vendor:common",
    "build:scripts:vendor:ckeditor"
]);

gulp.task('build:scripts:vendor:common', function () {
        var b = browserify({
            debug: debug
        });
        npmPackages.forEach(function (id) {
            b.require(id)
        });
        return b.bundle()
            .pipe(source('common.vendor.js'))
            .pipe(gulp.dest(pkginfo.dist));
});

gulp.task('build:scripts:vendor:ckeditor', function () {
        gulp.src([pkginfo.assets.bower+'/**/*'])
            .pipe(gulp.dest(pkginfo.dist));
});


gulp.task('build:styles', function () {
    gulp.src(pkginfo.assets.styles.entries).pipe(stylus({
        compress: true,
        'include css': true,
        include: pkginfo.stylus.includes
    }))
        .pipe(rename('bundle.css'))
        .pipe(gulp.dest(pkginfo.dist));
});


gulp.task('watch', ['build'], function () {
    gulp.watch(pkginfo.assets.scripts.watches, ['build:scripts']);
    gulp.watch(pkginfo.assets.styles.watches, ['build:styles']);
});


gulp.task('clean', function (callback) {
    glob = pkginfo.dist + '/*';
    del([glob, '!.gitignore'], callback);
});
