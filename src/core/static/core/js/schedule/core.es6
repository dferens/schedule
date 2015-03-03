var Schedule = window.Schedule || {}

Schedule.core = {
    getGroupLessons(groupCode, callback) {
        $.get(Schedule.settings.lessonsUrl, {group: groupCode})
         .success(result => callback(result.lessons))
    },

    getTeacherLessons(teacherId, callback) {
        $.get(Schedule.settings.lessonsUrl, {teacher: teacherId})
         .success(result => callback(result.lessons))
    },

    getCourseLessons(courseId, callback) {
        $.get(Schedule.settings.lessonsUrl, {course: courseId})
         .success(result => callback(result.lessons))
    },

    getWeekdayName(weekday) {
        let weekday = typeof weekday == 'string' ? parseInt(weekday) : weekday
        switch (weekday) {
            case 1: return "mn"
            case 2: return "tu"
            case 3: return "we"
            case 4: return "th"
            case 5: return "fr"
            case 6: return "sa"
            case 7: return "su"
        }
    }
}
