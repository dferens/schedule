var schedule = window.schedule || {}

schedule.ui = (function() {
  let Router = ReactRouter
  let {DefaultRoute, Link, Route, RouteHandler} = Router
  let {indexBy, groupBy, sortBy, has, map, mapValues, reduce, range} = _

  let {core} = schedule

  let CourseButton = React.createClass({
    render() {
      let {id, short_name} = this.props.course
      return (
        <div className="course-link">
          <Link to="course-schedule" params={{courseId: id}}>{short_name}</Link>
        </div>
      )
    }
  })

  let TeacherButton = React.createClass({
    render() {
      let {id, short_name} = this.props.teacher
      return (
        <Link to="teacher-schedule" params={{teacherId: id}}>{short_name}</Link>
      )
    }
  })

  let GroupButton = React.createClass({
    /*
     * Displays link to group schedule
     *
     * @prop {GroupBlock} group - group's code
     */
    render() {
      let {group} = this.props
      return (
        <Link className="group-link" to="group-schedule" params={{code: group.code}}>
          {group.code.toUpperCase()}
        </Link>
      )
    }
  })

  let LessonItem = React.createClass({
    /*
     * Displays single lesson object
     *
     * @prop {LessonBlock} lesson
     */
    render() {
      let {lesson} = this.props

      if (lesson) {
        let sortedGroups = sortBy(this.props.lesson.groups, 'code')
        let groupButtons = reduce(sortedGroups, (result, group) => {
          if (result.length > 0)
            result.push(", ")

          result.push(<GroupButton group={group}/>)
          return result
        }, [])

        let teacherButton = null
        if (lesson.teacher)
          teacherButton = <TeacherButton teacher={lesson.teacher} />

        return (
          <div className="lesson-item">
            <div className="lesson-item-content">
              <CourseButton course={lesson.course} />
              <div className="teacher-link">
                {teacherButton}
              </div>
              <p className="groups">{groupButtons}</p>
            </div>
          </div>
        )
      } else {
        return (
          <div className="lesson-item empty">
            <div className="lesson-item-content"/>
          </div>
        )
      }
    }
  })

  let LessonsList = React.createClass({
    /*
     * Displays collection of lessons for 1 day
     *
     * @prop {moment} lessonsDate
     * @prop {Array[LessonBlock]} lessons
     */
    headerMomentFormat: 'dddd, D MMMM',

    render() {
      let {lessons, lessonsDate} = this.props
      let isToday = moment().startOf('day').isSame(lessonsDate.startOf('day'))

      return (
        <div className={'lessons-list ' + (isToday ? 'today' : '')}>
          <div className="lesson-list-header">
            <div className="label">
              {lessonsDate.format(this.headerMomentFormat)}
            </div>
          </div>
          <div className="lesson-list-body">
            {map(lessons, lesson => <LessonItem lesson={lesson}/>)}
          </div>
        </div>
      )
    }
  })

  let LessonsWeekList = React.createClass({
    /*
     * Displays schedule for 1 week
     *
     * @prop {Integer} week
     * @prop {moment} weekStartDate
     * @prop {Array[LessonBlock]} lessons
     */
    render() {
      let {week, weekStartDate, lessons} = this.props
      let className = (week == 1) ? 'primary' : 'secondary'
      let lessonsPerDay = groupBy(lessons, 'weekday')
      map(lessonsPerDay, (lessons, day) => {
        let minNumber = _.min(lessons, 'number').number
        for (let i in range(1, minNumber))
          lessons.unshift(null)
      })
      map(core.getWeekdaysRange(), day => {
        if (!has(lessonsPerDay, day))
          lessonsPerDay[day] = []
      })

      return (
        <div className={'lessons-week ' + className}>
          {map(lessonsPerDay, (lessons, weekday) => {
            let date = moment(weekStartDate).add(weekday - 1, 'days')
            return (
              <LessonsList
                weekday={weekday}
                lessonsDate={date}
                lessons={lessons} />
            )}
          )}
        </div>
      )
    }
  })

  let Schedule = React.createClass({
    /*
     * Displays schedule grid for 2 weeks
     *
     * @prop {ScheduleBlock} schedule
     */
    render() {
      let now = moment()
      let schedule = this.props.schedule
      let lessonsPerWeek = groupBy(schedule.lessons, 'week')
      let currentWeekStartDate = now.subtract(now.day() - 1, 'days')
      let nextWeekStartDate = moment(currentWeekStartDate).add(7, 'days')
      let currentWeek = schedule.current_week
      let nextWeek = 1 + (currentWeek % 2)

      return (
        <div className="schedule">
          <LessonsWeekList
            week={currentWeek}
            weekStartDate={currentWeekStartDate}
            lessons={lessonsPerWeek[currentWeek]} />
          <LessonsWeekList
            week={nextWeek}
            weekStartDate={nextWeekStartDate}
            lessons={lessonsPerWeek[nextWeek]} />
        </div>
      )
    }
  })

  let GroupScheduleHandler = React.createClass({
    componentWillMount() {this.loadSchedule()},
    componentWillReceiveProps() {this.loadSchedule()},

    loadSchedule() {
      core.getGroupSchedule(
        this.props.params.code,
        ({group, schedule}) => this.setState({group: group, schedule: schedule})
      )
    },

    render() {
      if (this.state) {
        return (
          <div>
            <p>Schedule for group: {this.props.params.code}</p>
            <Schedule schedule={this.state.schedule} />
          </div>
        )
      } else {
        return null
      }
    }
  })

  let TeacherScheduleHandler = React.createClass({
    componentWillMount() {this.loadSchedule()},
    componentWillReceiveProps() {this.loadSchedule()},

    loadSchedule() {
      core.getTeacherSchedule(
        this.props.params.teacherId,
        ({teacher, schedule}) => this.setState({teacher: teacher, schedule: schedule})
      )
    },

    render() {
      if (this.state) {
        return (
          <div>
            <p>Schedule for teacher: {this.state.teacher.full_name}</p>
            <Schedule schedule={this.state.schedule} />
          </div>
        )
      } else {
        return null
      }
    }
  })

  let CourseScheduleHandler = React.createClass({
    componentWillMount() {this.loadSchedule()},
    componentWillReceiveProps() {this.loadSchedule()},

    loadSchedule() {
      core.getCourseSchedule(
        this.props.params.courseId,
        ({schedule, course}) => this.setState({schedule: schedule, course: course})
      )
    },

    render() {
      if (this.state) {
        return (
          <div>
            <p>Schedule for course: {this.state.course.full_name}</p>
            <Schedule schedule={this.state.schedule} />
          </div>
        )
      } else {
        return null
      }
    }
  })

  return {
    run(element) {
      let App = React.createClass({
        render() {
          return (
            <div className="schedule-app">
              <RouteHandler params={this.props.params}/>
            </div>
          )
        }
      })

      let routes = (
        <Route name="app" path="/schedule/" handler={App}>
          <Route name="group-schedule" path="group/:code/" handler={GroupScheduleHandler} />
          <Route name="teacher-schedule" path="teacher/:teacherId/" handler={TeacherScheduleHandler} />
          <Route name="course-schedule" path="course/:courseId/" handler={CourseScheduleHandler} />
        </Route>
      )
      Router.run(routes, Router.HistoryLocation, (Handler, state) => {
          React.render(<Handler params={state.params}/>, element)
        }
      )
    }
  }
})()
