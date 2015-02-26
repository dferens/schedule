(function(schedule) {
  var Router = ReactRouter,
      DefaultRoute = Router.DefaultRoute,
      Link = Router.Link,
      Route = Router.Route,
      RouteHandler = Router.RouteHandler;

  var App = React.createClass({
    render: function() {
      return (
        <div>
          <RouteHandler/>
        </div>
      );
    }
  });

  var LessonItem = React.createClass({
    render: function() {
      var lesson = this.props.lesson;
      return (
        <div className="list-group-item">
          <p>{lesson}</p>
        </div>
      )
    }
  });

  var LessonGroup = React.createClass({
    render: function() {
      var lessonNodes = this.props.lessons.map(function(l) {
        return <LessonItem lesson={l}/>
      });
      return (
        <div className="list-group">
          {lessonNodes}
        </div>
      )
    }
  });

  var LessonList = React.createClass({
    render: function() {
      var lessonsDays = this.props.lessons.groupBy(function(l) {return l.weekday});
      var lessonNodes = Object.map(lessonsDays, function(weekday, lessons) {
        return <LessonGroup weekday={weekday} lessons={lessons}/>;
      });
      if (lessonNodes) {
        return (
          <div className="lessons-list" style={{border:'1px solid red'}}>
            {lessonNodes}
          </div>
        )
      }
    }
  });

  var GroupSchedule = React.createClass({
    mixins: [Router.State],

    loadLessons: function (group_code) {
      var self = this;
      var code = this.getParams().code;

      $.get(schedule.API_URL, {group:code}, function (result) {
        self.setState({lessons: result.lessons});
      });
    },

    getInitialState: function() {
      return {lessons: null}
    },

    componentWillMount: function() {this.loadLessons()},

    componentWillReceiveProps: function() {this.loadLessons()},

    render: function() {
      if (this.state.lessons) {
        var lessonsWeeks = this.state.lessons.groupBy(function(l) {return l.week});
        return (
          <div>
            <p>Schedule for group {this.getParams().code}</p>
            <LessonList lessons={lessonsWeeks[1]}/>
            <LessonList lessons={lessonsWeeks[2]}/>
            <Link to="group" params={{code:'ia-11'}}>IA-11</Link>
          </div>
        )
      } else {
        return <p>Loading</p>;
      }
    }
  });

  var Dashboard = React.createClass({
    render: function() {
      return (
        <p>Dashboard</p>
      )
    }
  });

  var routes = (
    <Route name="app" path="/schedule/" handler={App}>
      <Route name="group" path="group/:code/" handler={GroupSchedule}/>
      <DefaultRoute handler={Dashboard}/>
    </Route>
  );

  schedule.run = function(element) {
    Router.run(routes, Router.HistoryLocation, function (Handler) {
      React.render(<Handler/>, element);
    });
  };
})(window.schedule = window.schedule || {})

schedule.run(document.getElementById('schedule-app'));
