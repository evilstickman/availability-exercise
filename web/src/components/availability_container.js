import React, { Component } from 'react';

class AvailabilityContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  createProviderAvailabilityCell(provider_id, availability) {
    // Note - this prints the time with seconds included. if this is an issue I can modify the code to drop the seconds portion of the time.
    return(
      <ul className="list-unstyled">
        {
          availability.map((val, i) => {
            const current_date = new Date(val);
            
            return (
              <li key={val}>
                <time dateTime={val} className="book-time">{current_date.toLocaleString([],{dateStyle:"short", timeStyle: "short"})}</time>
                <button className="book btn-small btn-primary" onClick={() => {this.props.booking_function(provider_id, val)}}>Book</button>
              </li>
            )
        })}
      </ul>
    );
  }

  createTableRow() {
    const provider_availability = this.props.provider_availability;
    if(provider_availability) {
      return(
        Object.keys(provider_availability).map((key, index) => {
          const availability = provider_availability[key];
          return <tr key={key}>
            <td>{key}</td>
            <td>{this.createProviderAvailabilityCell(key,availability)}</td>
          </tr>
        })
      )
    }
    return "";
  }

  render() {
    const {
      provider_availability
    } = this.props;
    return (
      <availability-container>
        <h2>Available Times</h2>
        <table className="advisors table">
          <thead>
            <tr>
              <th>Advisor ID</th>
              <th>Available Times</th>
            </tr>
          </thead>
          <tbody>{this.createTableRow()}</tbody>
        </table>
      </availability-container>
    );
  }
}

export default AvailabilityContainer;
