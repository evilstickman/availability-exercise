import React, { Component } from 'react';
import AvailabilityContainer from './components/availability_container'
import BookedContainer from './components/booked_container'

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.fetchToday();
  }

  async fetchToday() {
    try {
      const res = await fetch("http://localhost:4433/today");
      const provider_availability_list = await fetch("http://localhost:4433/times_by_advisor_id");
      const json = await res.json();
      const provider_availability_json = await provider_availability_list.json();
      this.setState({
        today: json.today,
        provider_availability: provider_availability_json,
      });
    } catch (e) {
      console.error("Failed to fetch 'today' data", e);
    }
  }

  async bookAppointment(provider_id, timeslot) {
    console.log("booking", provider_id, timeslot);
  }

  render() {
    const {
      provider_availability
    } = this.state;
    return (
      <div className="App container">
        <h1>Book Time with an Advisor</h1>

        {this.state.today && <span id="today">Today is {this.state.today}.</span>}

        <form id="name-form" className="col-md-6">
          <div className="form-group">
            <label htmlFor="name-field">Your Name</label>
            <input type="text" id="name-field" className="form-control" />
          </div>
        </form>
        <AvailabilityContainer provider_availability={provider_availability} booking_function={this.bookAppointment} />
        <BookedContainer />
        
        
      </div>
    );
  }
}

export default App;
