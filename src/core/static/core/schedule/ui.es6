var schedule = window.schedule || {}

schedule.ui = (function() {
  let Router = ReactRouter
  let {DefaultRoute, Link, Route, RouteHandler} = Router
  let {indexBy, groupBy, each, sortBy, has, map, mapValues, reduce, range} = _

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
     * @prop {bool} highlight
     */
    render() {
      let {lesson, highlight} = this.props

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

        let placeBadge = null
        if (lesson.place)
          placeBadge = <div className="place-badge">{lesson.place}</div>

        return (
          <div className={'lesson-item' + (highlight ? ' highlight':'')}>
            <div className="lesson-item-content">
              {placeBadge}
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
     * @prop {Integer} highlightLesson
     */
    headerMomentFormat: 'dddd, D MMMM',

    render() {
      let {lessons, lessonsDate, highlightLesson} = this.props

      return (
        <div className="lessons-list">
          <div className="lesson-list-header">
            <div className="label">
              {lessonsDate.format(this.headerMomentFormat)}
            </div>
          </div>
          <div className="lesson-list-body">
            {map(sortBy(lessons), lesson =>
              <LessonItem
                lesson={lesson}
                highlight={lesson != null && lesson.id == highlightLesson}/>
            )}
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
     * @prop {Integer} highlightLesson
     */
    render() {
      let {week, weekStartDate, lessons, highlightLesson} = this.props
      let className = (week == 1) ? 'primary' : 'secondary'
      let lessonsPerDay = groupBy(sortBy(lessons, 'number'), 'weekday')
      map(lessonsPerDay, (lessons, day) => {
        let minNumber = _.min(lessons, 'number').number
        for (let i in range(1, minNumber))
          lessons.unshift(null)
      })
      // Add dummy lesson lists for days without lessons
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
                key={weekday}
                weekday={weekday}
                lessonsDate={date}
                lessons={lessons}
                highlightLesson={highlightLesson}
                />
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
      let schedule = this.props.schedule
      let lessonsPerWeek = groupBy(schedule.lessons, 'week')
      let currentWeek = schedule.current_week
      let currentWeekStartDate = moment().weekday(0)

      if (moment().weekday() == 6) { // Sunday
        currentWeek = 1 + (currentWeek % 2)
        currentWeekStartDate.add(7, 'days')
      }

      let nextWeekStartDate = moment(currentWeekStartDate).add(7, 'days')
      let nextWeek = 1 + (currentWeek % 2)
      let highlightLessonId = (
        _.chain(lessonsPerWeek[currentWeek])
         .sortByAll(['weekday', 'number'])
         .filter(l => {
            let lessonDate = moment(currentWeekStartDate).add(l.weekday - 1, 'days')
            let [, lessonEnd] = core.getLessonRange(lessonDate, l.number)
            return moment().isBefore(lessonEnd)
         })
         .first()
         .value().id
      )

      return (
        <div className="schedule">
          <LessonsWeekList
            week={currentWeek}
            weekStartDate={currentWeekStartDate}
            lessons={lessonsPerWeek[currentWeek]}
            highlightLesson={highlightLessonId}/>
          <LessonsWeekList
            week={nextWeek}
            weekStartDate={nextWeekStartDate}
            lessons={lessonsPerWeek[nextWeek]} />
        </div>
      )
    }
  })

  let PrintSchedule = React.createClass({
    /*
     * Constructs printable schedule
     *
     * @prop {ScheduleBlock} schedule
     * @prop {String} title
     */

    formatTime(startTime, endTime) {
      return `${startTime.format('H:mm')} - ${endTime.format('H:mm')}`
    },

    formatLesson({course, teacher, place, type}) {
      let lessonType = {
        lecture: 'Лек',
        practice: 'Прак',
        lab: 'Лаб',
        null: ''
      }[type]
      let teacherName = teacher? teacher.short_name : ''
      return `${course.short_name}, ${teacherName} ${place || ''} ${lessonType}`
    },

    lessonsEqual(l1, l2) {
      return (
        _.isEqual(l1.course, l2.course) &&
        _.isEqual(l1.teacher, l2.teacher) &&
        (l1.number == l2.number) &&
        (l1.place == l2.place) &&
        (l1.type == l2.type) &&
        (l1.weekday == l2.weekday)
      )
    },

    render() {
      let {schedule, title} = this.props
      let lessonsByWeekday = groupBy(schedule.lessons, 'weekday')

      let renderLessonCell = (content, colSpan=1) => {
        return <td className="lesson-cell" colSpan={colSpan}>{content}</td>
      }

      let addWeekdayRow = (nodes, dayLessons, weekday) => {
        let dayLessons = sortBy(dayLessons, 'number')
        let weekdayName = moment().weekday(weekday - 1).format('dddd')
        let lessonsPerNumber = groupBy(dayLessons, 'number')
        let numbersCount = _.keys(lessonsPerNumber).length

        each(lessonsPerNumber, (lessons, number) => {
          let [lessonStart, lessonEnd] = core.getLessonRange(moment(), number)

          if (lessons.length == 2) {
            if (this.lessonsEqual(lessons[0], lessons[1])) {
              var lessonCells = [renderLessonCell(this.formatLesson(lessons[0]), 2)]
            } else {
              var lessonCells = map(lessons, l => renderLessonCell(this.formatLesson(l)))
            }
          } else {
            let emptyCell = renderLessonCell('')
            let lessonCell = renderLessonCell(this.formatLesson(lessons[0]))
            var lessonCells = (lessons[0].week == 1) ?
                                [lessonCell, emptyCell] :
                                [emptyCell, lessonCell]
          }

          let weekdayNode = null
          if (number == dayLessons[0].number)
            weekdayNode = (
              <td className="weekday-cell"
                  rowSpan={numbersCount}>{weekdayName}</td>
            )

          nodes.push(
            <tr data-weekday={weekday}>
              {weekdayNode}
              <td className="number-cell">{number}</td>
              <td className="time-cell">{this.formatTime(lessonStart, lessonEnd)}</td>
              {lessonCells}
            </tr>
          )
        })
        return nodes
      }

      let rowsNodes = reduce(lessonsByWeekday, addWeekdayRow, [])

      return (
        <div className="printable-schedule">
          <table className="schedule">
            <tbody>
              <!-- Header starts-->
              <tr>
                <th rowSpan="2"></th>
                <th rowSpan="2">№</th>
                <th rowSpan="2">час</th>
                <th colSpan="2">{title}</th>
              </tr>
              <tr>
                <td>I тиждень</td>
                <td>II тиждень</td>
              </tr>
              <!-- Header ends -->
              {rowsNodes}
            </tbody>
          </table>
        </div>
      )
    }
  })

  let GroupScheduleHandler = React.createClass({
    componentWillMount() {
      this.loadSchedule(this.props.params.code)
    },
    componentWillReceiveProps(nextProps) {
      this.loadSchedule(nextProps.params.code)
    },

    loadSchedule(groupCode) {
      core.getGroupSchedule(groupCode, ({group, schedule}) => {
        this.setState({group: group, schedule: schedule})
      })
    },

    render() {
      if (this.state == null)
        return null

      return (
        <div>
          <div className="hidden-print">
            <div className="row">
              <div className="col-md-10">
                <p className="lead">Schedule for group: {this.props.params.code}</p>
              </div>
              <div className="col-md-2">
                <button className="btn btn-primary btn-lg pull-right"
                  onClick={print}>Print</button>
              </div>
            </div>
            <div className="row">
              <div className="col-md-12">
                <Schedule schedule={this.state.schedule} />
              </div>
            </div>
          </div>
          <div className="visible-print-block">
            <PrintSchedule
              schedule={this.state.schedule}
              title={`Група ${this.state.group.code.toUpperCase()}`} />
          </div>
        </div>
      )
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
      if (this.state == null)
        return null

      return (
        <div>
          <div className="row">
            <div className="col-md-12">
              <p className="lead">Schedule for: {this.state.teacher.full_name}</p>
            </div>
          </div>
          <div className="row">
            <div className="col-md-12">
              <Schedule schedule={this.state.schedule} />
            </div>
          </div>
        </div>
      )
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
            <div className="row">
              <div className="col-md-12">
                <p className="lead">Schedule for course: {this.state.course.full_name}</p>
              </div>
            </div>
            <div className="row">
              <div className="col-md-12">
                <Schedule schedule={this.state.schedule} />
              </div>
            </div>
          </div>
        )
      } else {
        return null
      }
    }
  })

  let StartHandlerResults = React.createClass({
    contextTypes: {
      router: React.PropTypes.func.isRequired
    },

    getInitialState() {
      return {teachers: [], courses: [], groups: []}
    },

    componentWillReceiveProps(newProps) {
      core.searchItems(newProps.query, data => {
        let {teachers, groups, courses} = data.results
        this.setState({
          teachers: sortBy(teachers, 'full_name'),
          groups: sortBy(groups, 'code'),
          courses: sortBy(courses, 'full_name')
        })
      })
    },

    renderObjectLink(object, type=null) {
      let linkNode = null;

      if (type == 'group') {
        linkNode = (
          <Link to="group-schedule" params={{code: object.code}}>
            <span className="glyphicon glyphicon-pencil" aria-hidden="true">
            </span> {object.code.toUpperCase()}
          </Link>
        )
      } else if (type == 'teacher') {
        linkNode = (
          <Link to="teacher-schedule" params={{teacherId: object.id}}>
            <span className="glyphicon glyphicon-user" aria-hidden="true">
            </span> {object.full_name}
          </Link>
        )
      } else {
        linkNode = (
          <Link to="course-schedule" params={{courseId: object.id}}>
            <span className="glyphicon glyphicon-book" aria-hidden="true">
            </span> [{object.short_name}] {object.full_name}
          </Link>
        )
      }
      return (
        <div className="list-group-item">
          {linkNode}
        </div>
      )
    },

    render() {
      let {teachers, groups, courses} = this.state

      return (
        <div className="search-results">
          <div className="list-group">
            {map(teachers, t => this.renderObjectLink(t, 'teacher'))}
            {map(groups, g => this.renderObjectLink(g, 'group'))}
            {map(courses, c => this.renderObjectLink(c, 'course'))}
          </div>
        </div>
      )
    }
  })

  let StartHandler = React.createClass({
    getInitialState() {
      return {value: ''}
    },

    handleChange(event) {
      this.setState({value: event.target.value})
    },

    render() {
      return (
        <div className="start-page">
          <div className="row">
            <div className="col-md-12">
              <div className="input-group input-group-lg">
                <input
                  type="text" className="form-control"
                  value={this.state.value}
                  onChange={this.handleChange}
                  placeholder="Type group, teacher or course name"/>
                <span className="input-group-addon">@</span>
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col-md-12">
              <StartHandlerResults query={this.state.value}/>
            </div>
          </div>
        </div>
      )
    }
  })

  return {
    run(element) {
      let App = React.createClass({
        render() {
          return <RouteHandler params={this.props.params}/>
        }
      })

      let routes = (
        <Route name="app" path="/schedule/" handler={App}>
          <Route name="group-schedule" path="group/:code/" handler={GroupScheduleHandler} />
          <Route name="teacher-schedule" path="teacher/:teacherId/" handler={TeacherScheduleHandler} />
          <Route name="course-schedule" path="course/:courseId/" handler={CourseScheduleHandler} />
          <DefaultRoute handler={StartHandler} />
        </Route>
      )
      Router.run(routes, Router.HistoryLocation, (Handler, state) => {
          React.render(<Handler params={state.params}/>, element)
        }
      )
    }
  }
})()
