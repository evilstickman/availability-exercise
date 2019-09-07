import React, { Component } from 'react';

class BookedContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {booked: []};
    this.createBookingTable = this.createBookingTable.bind(this);
    this.createBookingRow = this.createBookingRow.bind(this);
    this.getBookedTimes = this.getBookedTimes.bind(this);
    this.getBookedTimes();
  }

  async getBookedTimes() {
    try {
      const res = await fetch("http://localhost:4433/booked_times");
      const json = await res.json();
      this.setState({
        booked: json,
      });
    } catch (e) {
      console.error("Failed to fetch 'today' data", e);
    }
  }

  

  createBookingRow(bookedJson) {
    // Note - this prints the time with seconds included. if this is an issue I can modify the code to drop the seconds portion of the time.
    const name = bookedJson.name;
    const provider_id = bookedJson.provider_id;
    const timestamp = new Date(bookedJson.timestamp);
    return(
      <tr>
        <td>{provider_id}</td>
        <td>{name}</td>
        <td>{timestamp.toLocaleString([],{dateStyle:"short", timeStyle: "short"})}</td>
      </tr>
    );
  }

  createBookingTable() {
    let booked = [];
    if(this.state) {
      booked = this.state.booked;
    }
    console.log(booked);

    return (
      booked.map((key, index) => {
        console.log(key)
        return this.createBookingRow(key)
      }));
  }

  render() {
    return (
      <booked-container>
        <h2>Booked Times</h2>
        <table className="bookings table">
          <thead>
            <tr>
              <th>Advisor ID</th>
              <th>Student Name</th>
              <th>Date/Time</th>
            </tr>
          </thead>
          <tbody>
            {this.createBookingTable()}
          </tbody>
        </table>
      </booked-container>
    );
  }
}

export default BookedContainer;
