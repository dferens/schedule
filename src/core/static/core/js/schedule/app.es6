(function (module) {
  let Router = ReactRouter;
  let {DefaultRoute, Link, Route, RouteHandler} = Router;

  let App = React.createClass({
    render() {
      return <div>
        <RouteHandler/>
      </div>
    }
  })

  let LessonItem = React.createClass({
    render() {
      return <div className="list-group-item">
        <p>{this.props.lesson}</p>
      </div>
    }
  })

  let LessonGroup = React.createClass({
    render() {
      return <div className="list-group">
        {this.props.lessons.map(l => <LessonItem lesson={l}/>)}
      </div>
    }
  })

  let LessonList = React.createClass({
    render() {
      let lessonsPerDays = this.props.lessons.reduce(
        (result, lesson) => {
          result.set(lesson.weekday, result.get(lesson.weekday) || [])
          result.get(lesson.weekday).push(lesson)
          return result
        },
        new Map()
      )
      return <div className="lessons-list" style={{border: '1px solid red'}}>
        {[for ([weekday, lessons] of lessonsPerDays)
          <LessonGroup lessons={lessons}/>]}
      </div>
    }
  })

  let GroupSchedule = React.createClass({
    mixins: [Router.State],

    loadLessons(group_code) {
      let code = this.getParams().code

      $.get(schedule.API_URL, {group:code}, result => {
        this.setState({lessons: result.lessons})
      })
    },

    getInitialState() {
      return {lessons: null}
    },

    componentWillMount() {this.loadLessons()},

    componentWillReceiveProps() {this.loadLessons()},

    render() {
      if (this.state.lessons) {
        let lessonsPerWeeks = this.state.lessons.reduce(
          (result, lesson) => {
            result.set(lesson.week, result.get(lesson.week) || [])
            result.get(lesson.week).push(lesson)
            return result
          },
          new Map()
        )
        return <div>
          <p>Schedule for group {this.getParams().code}</p>
          <LessonList lessons={lessonsPerWeeks.get(1)}/>
          <LessonList lessons={lessonsPerWeeks.get(2)}/>
          <Link to="group" params={{code:'ia-11'}}>IA-11</Link>
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

  let routes = (
    <Route name="app" path="/schedule/" handler={App}>
      <Route name="group" path="group/:code/" handler={GroupSchedule}/>
      <DefaultRoute handler={Dashboard}/>
    </Route>
  )

  module.run = (element) => {
    Router.run(routes, Router.HistoryLocation, H => React.render(<H/>, element))
  }
})(window.schedule = window.schedule || {})
