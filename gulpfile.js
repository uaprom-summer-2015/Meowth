var gulp = require('gulp');
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
var pkginfo = require('./package.json');

var debug = gutil.env.type !== 'production';

var npmPackages = Object.keys(pkginfo.dependencies) || [];

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
            b.external(npmPackages);


            b.external("npm-zepto");

            return b
                .bundle()
                .pipe(source(path.basename(file)))
                .pipe(rename({
                    extname: ".bundle.js"
                }))
                .pipe(buffer())
                .pipe(debug ? gutil.noop() : uglify())
                .pipe(gulp.dest(pkginfo.dist.path + pkginfo.dist.js));
        });
        es.merge(tasks).on('end', done);
    });
});

gulp.task('build:scripts:vendor', [
    "build:scripts:vendor:common",
    "build:scripts:vendor:ckeditor"
]);

gulp.task('build:scripts:vendor:common', function (done) {
    var b = browserify({
        debug: debug
    });

    var bundle = b.require(npmPackages)
        .require("npm-zepto")
        .bundle()
        .pipe(source('common.vendor.js'))
        .pipe(buffer())
        .pipe(debug ? gutil.noop() : uglify())
        .pipe(gulp.dest(pkginfo.dist.path + pkginfo.dist.js));


    var bs_fonts = gulp.src([pkginfo.assets.node + '/bootstrap/fonts/**/*'])
        .pipe(gulp.dest(pkginfo.dist.path + pkginfo.dist.fonts));


    es.merge([bundle, bs_fonts]).on('end', done);
});

gulp.task('build:scripts:vendor:ckeditor', function () {
    gulp.src([pkginfo.assets.bower + '/**/*'])
        .pipe(gulp.dest(pkginfo.dist.path + pkginfo.dist.js));
});


gulp.task('build:styles', function () {
    gulp.src(pkginfo.assets.styles.entries).pipe(stylus({
        compress: true,
        'include css': true,
        include: pkginfo.stylus.includes
    }))
        .pipe(rename('bundle.css'))
        .pipe(gulp.dest(pkginfo.dist.path + pkginfo.dist.styles));
});


gulp.task('watch', ['default'], function () {
    gulp.watch(pkginfo.assets.scripts.watches, ['build:scripts:app']);
    gulp.watch(pkginfo.assets.styles.watches, ['build:styles']);
});


gulp.task('clean', function (callback) {
    glob = pkginfo.dist.path + '/*';
    del([glob, '!.gitignore'], callback);
});
