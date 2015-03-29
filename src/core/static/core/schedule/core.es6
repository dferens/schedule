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

    searchItems(query, callback) {
        let url = schedule.settings.search_url
        $.get(url, {query: query}, data => {
            callback({results: data.results})
        })
    },

    getWeekdaysRange() {
        return _.range(1, 7)
    },

    getLessonNumbersRange() {
        return _.range(1, 6)
    },

    getLessonRange(date, lessonNumber) {
        if (lessonNumber < 1 || lessonNumber > 5)
            throw 'Invalid lesson number'

        let start = moment(date).hours(8).minutes(30).seconds(0)
        start.add(115 * (lessonNumber - 1), 'minutes')
        return [
            start,
            moment(start).add(95, 'minutes')
        ]
    }
}
