const gulp = require("gulp");
const shell = require("gulp-shell");
const watch = require("gulp-watch");

gulp.task("build", shell.task(["npm run build"]));

gulp.task("watch", () => {
  watch(["src/**/*", "public/**/*"], gulp.series("build"));
});

gulp.task("default", gulp.series("build", "watch"));
