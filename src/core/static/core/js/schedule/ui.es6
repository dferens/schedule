var Schedule = window.Schedule || {}

Schedule.ui = (function() {
  let Router = ReactRouter
  let {DefaultRoute, Link, Route, RouteHandler} = Router
  let {clone, indexBy, groupBy, has, map, reduce, range} = _

  let {core} = Schedule

  let App = React.createClass({
    render() {
      return <div>
        <RouteHandler/>
      </div>
    }
  })

  let GroupButton = React.createClass({
    render() {
      return (
        <Link to="group" params={{code:this.props.code}}>
          {this.props.code.toUpperCase()}
        </Link>
      )
    }
  })

  let LessonItem = React.createClass({
    render() {
      let lesson = this.props.lesson

      if (lesson) {
        let sortedGroups = clone(this.props.lesson.groups).sort()
        let groupNodes = reduce(sortedGroups, (result, groupCode) => {
          if (result.length > 0)
            result.push(", ")

          result.push(<GroupButton code={groupCode}/>)
          return result
        }, [])

        return (
          <div className="lesson-item">
            <h5 className="title">
              {lesson.course.short_name}
            </h5>
            <p className="teacher">{lesson.teacher.short_name}</p>
            <p className="groups">{groupNodes}</p>
          </div>
        )
      } else {
        return <div className="lesson-item empty"/>
      }
    }
  })

  let LessonsList = React.createClass({
    render() {
      let lessonPerNum = indexBy(this.props.lessons, "number")
      range(1, 6).filter(num => !has(lessonPerNum, num))
                 .forEach(num => {lessonPerNum[num] = null})

      return (
        <div className="">
          <div className="lessons-list">
            <div className="lesson-item header">
              <p>{Schedule.core.getWeekdayName(this.props.weekday)}</p>
            </div>
            {map(lessonPerNum, (lesson, num) =>
              <LessonItem lesson={lesson}/>)}
          </div>
        </div>
      )
    }
  })

  let LessonsWeek = React.createClass({
    render() {
      let lessonsPerDays = groupBy(this.props.lessons, "weekday")
      return <div className="row">
        {map(lessonsPerDays, (lessons, weekday) =>
          <LessonsList weekday={weekday} lessons={lessons}/>)}
      </div>
    }
  })

  let GroupSchedule = React.createClass({
    mixins: [Router.State],

    loadLessons(group_code) {
      core.getGroupLessons(
        this.getParams().code,
        lessons => this.setState({lessons: lessons})
      )
    },

    getInitialState() {
      return {lessons: null}
    },

    componentWillMount() {this.loadLessons()},

    componentWillReceiveProps() {this.loadLessons()},

    render() {
      if (this.state.lessons) {
        let lessonsPerWeeks = groupBy(this.state.lessons, "week")
        return <div>
          <p>Schedule for group {this.getParams().code}</p>
          <LessonsWeek lessons={lessonsPerWeeks[1]}/>
          <LessonsWeek lessons={lessonsPerWeeks[2]}/>
        </div>
      } else {
        return <p>Loading</p>
      }
    }
  })

  let Dashboard = React.createClass({
    render() {
      return <p>Dashboard</p>
    }
  })

  return {
    run(element) {
      let routes = (
        <Route name="app" path="/schedule/" handler={App}>
          <Route name="group" path="group/:code/" handler={GroupSchedule}/>
          <DefaultRoute handler={Dashboard}/>
        </Route>
      )
      Router.run(routes, Router.HistoryLocation, H => React.render(<H/>, element))
    }
  }
})()
