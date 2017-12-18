var gulp = require('gulp');
var os = require('os');
var prettify = require('gulp-jsbeautifier');
var jshint = require('gulp-jshint');
var nodemon = require('gulp-nodemon');
var spawn = require('child_process').spawn;
var mongodbData = require('gulp-mongodb-data');
var gulp = require('gulp-help')(require('gulp'));
var runSequence = require('run-sequence');

gulp.task('prettify', 'Prettify all server side js.', function () {
    gulp.src(['./*.js', '!./gulpfile.js', './middleware/**/*.js', './public/**/*.js', './routes/**/*.js', './schemas/**/*.js', './*.js'], {
            base: './'
        })
        .pipe(prettify())
        .pipe(gulp.dest('./'));
});

gulp.task('lint', 'Lints all server side js.', function () {
    gulp.src(['./*.js', './middleware/**/*.js', './routes/**/*.js', './schemas/**/*.js', './*.js'], {
            base: './'
        })
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

gulp.task('metadata', 'Imports default portals definitions.', function () {
    console.log("Importing Collections");
    gulp.src('./metadata/portals.json')
        .pipe(mongodbData({
            mongoUrl: 'mongodb://localhost/ID-dev',
            collectionName: 'portals',
            dropCollection: true
        }));
});

gulp.task('install', 'Install packages using yarn.', function (cb) {
    if (os.platform() === 'win32') {
        var command = 'yarn.cmd'
    } else {
        var command = 'yarn'
    }
    var cmd = spawn(command, ['install'], {
        stdio: 'inherit'
    });
    cmd.on('close', function (code) {
        console.log('install exited with code ' + code);
        cb(code);
    });
});

gulp.task('run', 'Run node server.', function (cb) {
    var cmd = spawn('node', ['./bin/www'], {
        stdio: 'inherit'
    });
    cmd.on('close', function (code) {
        console.log('run exited with code ' + code);
        cb(code);
    });
    cmd.on('error', function (err) {
        console.error(err);
        process.exit(1);
    });
    cmd.on('exit', function (code) {
        if (code !== 0) {
            console.log('Bower failed.');
        }
    });
});

gulp.task('check', 'Prettifying and checks linting.', function () {
    runSequence('install', 'prettify', 'lint', 'run');
});