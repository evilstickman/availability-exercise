import React, { Component } from 'react';
import AvailabilityContainer from './components/availability_container'
import BookedContainer from './components/booked_container'

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {};

    this.changeName = this.changeName.bind(this);
    this.fetchToday = this.fetchToday.bind(this);
    this.bookAppointment = this.bookAppointment.bind(this);
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

  changeName(event) {
    this.setState({
      name: event.target.value,
    });
  }

  async bookAppointment(provider_id, timeslot) {
    if(!this.state || !this.state.name || this.state.name === "") {
      alert("Please enter a name before booking an appointment");
    }
    else {
      console.log("booking", provider_id, timeslot);
      try {
        await fetch('http://localhost:4433/book', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            provider_id: provider_id,
            timestamp: timeslot,
            name: this.state.name,
          })
        });
        // Force a render as the underlying state changes are not propogating upwards.
        window.location.reload();
      } catch (e) {
        console.error("Booking failed", e);
      }
    }
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
            <input type="text" id="name-field" className="form-control" onChange={this.changeName} />
          </div>
        </form>
        <AvailabilityContainer provider_availability={provider_availability} booking_function={this.bookAppointment} />
        <BookedContainer />
        
        
      </div>
    );
  }
}

export default App;
