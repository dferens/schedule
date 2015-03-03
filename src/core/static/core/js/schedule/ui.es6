var Schedule = window.Schedule || {}

Schedule.ui = (function() {
  let Router = ReactRouter
  let {DefaultRoute, Link, Route, RouteHandler} = Router
  let {clone, indexBy, groupBy, has, map, mapValues, reduce, range} = _

  let {core} = Schedule

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
     * @prop {String} code - group's code
     */
    render() {
      return (
        <Link className="group-link" to="group-schedule" params={{code: this.props.code}}>
          {this.props.code.toUpperCase()}
        </Link>
      )
    }
  })

  let LessonItem = React.createClass({
    /*
     * Displays single lesson object
     *
     * @prop Object lesson
     */
    render() {
      let {lesson} = this.props

      if (lesson) {
        let sortedGroups = clone(this.props.lesson.groups).sort()
        let groupButtons = reduce(sortedGroups, (result, groupCode) => {
          if (result.length > 0)
            result.push(", ")

          result.push(<GroupButton code={groupCode}/>)
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
     * @prop {Array[Object]} lessons
     */
    render() {
      let lessonPerNum = indexBy(this.props.lessons, "number")
      range(1, 6).filter(num => !has(lessonPerNum, num))
                 .forEach(num => {lessonPerNum[num] = null})

      return (
        <div className="lessons-list">
          <div className="lesson-item header">
            <p>{Schedule.core.getWeekdayName(this.props.weekday)}</p>
          </div>
          {map(lessonPerNum, lesson => <LessonItem lesson={lesson}/>)}
        </div>
      )
    }
  })

  let LessonsTable = React.createClass({
    /*
     * Displays schedule grid for 2 weeks
     *
     * @prop {Array[Object]} lessons
     */
    render() {
      let lessonsPerWeek = mapValues(
        groupBy(this.props.lessons, 'week'),
        lessons => groupBy(lessons, 'weekday')
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

  let GroupSchedule = React.createClass({
    mixins: [Router.State],

    getInitialState() {return {lessons: []}},
    componentWillMount() {this.loadLessons()},
    componentWillReceiveProps() {this.loadLessons()},

    loadLessons() {
      core.getGroupLessons(
        this.getParams().code,
        lessons => this.setState({lessons: lessons})
      )
    },

    render() {
      return (
        <div>
          <p>Schedule for group {this.getParams().code}</p>
          <LessonsTable lessons={this.state.lessons} />
        </div>
      )
    }
  })

  let TeacherSchedule = React.createClass({
    mixins: [Router.State],

    getInitialState() {return {lessons: []}},
    componentWillMount() {this.loadLessons()},
    componentWillReceiveProps() {this.loadLessons()},

    loadLessons() {
      core.getTeacherLessons(
        this.getParams().teacherId,
        lessons => this.setState({lessons: lessons})
      )
    },

    render() {
      return (
        <div>
          <p>Schedule for teacher</p>
          <LessonsTable lessons={this.state.lessons} />
        </div>
      )
    }
  })

  let CourseSchedule = React.createClass({
    mixins: [Router.State],

    getInitialState() {return {lessons: []}},
    componentWillMount() {this.loadLessons()},
    componentWillReceiveProps() {this.loadLessons()},

    loadLessons() {
      core.getCourseLessons(
        this.getParams().courseId,
        lessons => this.setState({lessons: lessons})
      )
    },

    render() {
      return (
        <div>
          <p>Schedule for course</p>
          <LessonsTable lessons={this.state.lessons} />
        </div>
      )
    }
  })

  return {
    run(element) {
      let App = React.createClass({
        render() {
          return <div><RouteHandler/></div>
        }
      })

      let routes = (
        <Route name="app" path="/schedule/" handler={App}>
          <Route name="group-schedule" path="group/:code/" handler={GroupSchedule} />
          <Route name="teacher-schedule" path="teacher/:teacherId/" handler={TeacherSchedule} />
          <Route name="course-schedule" path="course/:courseId/" handler={CourseSchedule} />
        </Route>
      )
      Router.run(routes, Router.HistoryLocation, H => React.render(<H/>, element))
    }
  }
})()
