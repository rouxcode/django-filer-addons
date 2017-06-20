'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');


var sass_conf = {
    errLogToConsole: true,
    outputStyle: 'compressed'
};



gulp.task('sass', function () {
    return gulp.src('filer_addons/filer_gui/static/admin/filer_gui/scss/**/*.scss')
        .pipe(sass(sass_conf).on('error', sass.logError))
        .pipe(gulp.dest('filer_addons/filer_gui/static/admin/filer_gui/css'));
});

gulp.task('watch', function () {
    gulp.watch('filer_addons/filer_gui/static/admin/filer_gui/scss/**/*.scss', ['sass']);
});
