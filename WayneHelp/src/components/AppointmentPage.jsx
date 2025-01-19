import React, { useState } from "react";
import "./AppointmentPage.css";

const AppointmentPage = () => {
  const [selectedExpert, setSelectedExpert] = useState("");
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedTime, setSelectedTime] = useState("");

  const experts = [
    "Dr. Jane Doe - Psychologist",
    "Dr. John Smith - Psychiatrist",
    "Dr. Alice Johnson - Therapist",
    "Dr. Mark Lee - Counselor",
    "Dr. Emily Davis - Clinical Psychologist",
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedExpert && selectedDate && selectedTime) {
      alert(
        `Appointment booked with ${selectedExpert} on ${selectedDate} at ${selectedTime}`
      );
    } else {
      alert("Please select an expert, date, and time.");
    }
  };

  return (
    <div className="appointment-page">
      <h1>Appointment Page</h1>
      <form onSubmit={handleSubmit} className="appointment-form">
        <div className="form-section">
          <h2>Select Expert</h2>
          <div className="expert-list">
            {experts.map((expert, index) => (
              <label key={index} className="expert-item">
                <input
                  type="radio"
                  name="expert"
                  value={expert}
                  onChange={(e) => setSelectedExpert(e.target.value)}
                />
                {expert}
              </label>
            ))}
          </div>
        </div>
        <div className="form-section">
          <h2>Select Date/Time</h2>
          <div className="datetime-selection">
            <div className="date-selection">
              <label htmlFor="date">Date:</label>
              <input
                type="date"
                id="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
              />
            </div>
            <div className="time-selection">
              <label htmlFor="time">Time:</label>
              <select
                id="time"
                value={selectedTime}
                onChange={(e) => setSelectedTime(e.target.value)}
              >
                <option value="">Select Time</option>
                <option value="9:00 AM">9:00 AM</option>
                <option value="10:00 AM">10:00 AM</option>
                <option value="11:00 AM">11:00 AM</option>
                <option value="1:00 PM">1:00 PM</option>
                <option value="2:00 PM">2:00 PM</option>
                <option value="3:00 PM">3:00 PM</option>
              </select>
            </div>
          </div>
        </div>
        <button type="submit" className="submit-button">
          Book Appointment
        </button>
      </form>
    </div>
  );
};

export default AppointmentPage;
