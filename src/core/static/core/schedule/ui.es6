var schedule = window.schedule || {}

schedule.ui = (function() {
  let Router = ReactRouter
  let {DefaultRoute, Link, Route, RouteHandler} = Router
  let {indexBy, groupBy, sortBy, has, map, mapValues, reduce, range} = _

  let {core} = schedule

  function setDefaults(object, keys, value=null) {
    keys.filter(k => !has(object, k))
        .forEach(k => {object[k] = value})
    return object
  }

  let CourseButton = React.createClass({
    render() {
      let {id, short_name} = this.props.course
      return (
        <Link className="course-link" to="course-schedule" params={{courseId: id}}>
          {short_name}
        </Link>
      )
    }
  })

  let TeacherButton = React.createClass({
    render() {
      let {id, short_name} = this.props.teacher
      return (
        <Link className="teacher-link" to="teacher-schedule" params={{teacherId: id}}>
          {short_name}
        </Link>
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
            <CourseButton course={lesson.course} />
            {teacherButton}
            <p className="groups">{groupButtons}</p>
          </div>
        )
      } else {
        return <div className="lesson-item empty"/>
      }
    }
  })

  let LessonsList = React.createClass({
    /*
     * Displays collection of lessons for 1 day
     *
     * @prop {Array[LessonBlock]} lessons
     */
    render() {
      let lessonPerNum = indexBy(this.props.lessons, "number")
      setDefaults(lessonPerNum, core.getLessonNumbersRange())
      return (
        <div className="lessons-list">
          <div className="lesson-item header">
            <p>{core.getWeekdayName(this.props.weekday)}</p>
          </div>
          {map(lessonPerNum, lesson => <LessonItem lesson={lesson}/>)}
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
      let schedule = this.props.schedule
      let lessonsPerWeek = mapValues(
        groupBy(schedule.lessons, 'week'),
        lessons => {
          let result = groupBy(lessons, 'weekday')
          setDefaults(result, core.getWeekdaysRange())
          return result
        }
      )

      return (
        <div>
          {map(lessonsPerWeek, (lessonsPerDay, week) =>
            <div className="row">
              {map(lessonsPerDay, (lessons, weekday) =>
                <LessonsList weekday={weekday} lessons={lessons}/>)}
            </div>)}
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
          return <div><RouteHandler params={this.props.params}/></div>
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
