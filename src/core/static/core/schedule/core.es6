var schedule = window.schedule || {}

schedule.core = {
    getGroupSchedule(groupCode, callback) {
        let url = schedule.settings.group_lessons_url
        $.get(url, {code: groupCode}, result => {
            callback({
                group: result.group,
                schedule: result.schedule
            })
        })
    },

    getTeacherSchedule(teacherId, callback) {
        let url = schedule.settings.teacher_lessons_url
        $.get(url, {teacher: teacherId}, result => {
            callback({
                teacher: result.teacher,
                schedule: result.schedule
            })
        })
    },

    getCourseSchedule(courseId, callback) {
        let url = schedule.settings.course_lessons_url
        $.get(url, {course: courseId}, result => {
            callback({
                course: result.course,
                schedule: result.schedule
            })
        })
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
