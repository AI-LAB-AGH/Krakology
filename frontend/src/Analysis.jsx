import React, { useState } from "react";
import Map from "./Map";
import "./index.css";

const Analysis = ({ hide }) => {
  const categories = {
    beer: "Piwo",
    "bread/bakery": "Pieczywo",
    beverages: "Napoje",
    dairy: "Nabiał",
    eggs: "Jajka",
  };
  const scales = {
    0: "Brak",
    1: "Bardzo mała",
    2: "Mała",
    3: "Średnia",
    4: "Duża",
    5: "Bardzo duża",
  };
  const event_types = {
    concert: "Koncert",
  };
  const [category, setCategory] = useState("Wybierz kategorię");
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [events, setEvents] = useState();
  const [locations, setLocations] = useState();

  const handleStartChange = async (event) => {
    const value = event.target.value;
    setStartDate(value);
  };

  const handleEndChange = (event) => {
    const value = event.target.value;
    setEndDate(value);
  };

  const handleCategoryChange = (event) => {
    const value = event.target.value;
    setCategory(value);
  };

  const analyse = async () => {
    const formData = new FormData();
    formData.append("category", category);
    formData.append("start", startDate);
    formData.append("end", endDate);
    await fetch("api/fetch/", {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data) {
          setEvents(data.events);
          console.log(data.events);
          setLocations(
            data.events.map((event) => [
              event.latitude,
              event.longitude,
              "Koncert",
            ])
          );
        }
      });
  };

  const getCSRFToken = () => {
    const cookieValue = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1];
    return cookieValue || "";
  };

  return (
    <div className={"analysis" + (hide ? " hide" : "")}>
      <div className="map">
        <Map locations={locations}></Map>
      </div>

      <div className="dropdown-wrap flex flex-col">
        <div className="dropdown">
          <select value={category} onChange={handleCategoryChange}>
            <option value="Wybierz kategorię" disabled>
              -&nbsp;Wybierz kategorię&nbsp;-
            </option>
            {Object.entries(categories).map(([key, value]) => (
              <option value={key}>{value}</option>
            ))}
          </select>
        </div>

        <div className="dropdown">
          Data początkowa: &nbsp;
          <input
            type="date"
            id="start"
            name="trip-start"
            value={startDate}
            min="2018-01-01"
            max="2018-12-31"
            onChange={handleStartChange}
          />
          <br></br>
          Data końcowa: &nbsp;
          <input
            type="date"
            id="end"
            name="trip-start"
            value={endDate}
            min="2018-01-01"
            max="2018-12-31"
            onChange={handleEndChange}
          />
          <div>
            <button className="button" onClick={analyse}>
              Generuj
            </button>
          </div>
        </div>

        <div className="scroll">
          {events
            ? events.map((event) => (
                <div className="event">
                  <div className="event-title">{event.artist}</div>
                  <div className="event-el">
                    <b>Lokalizacja:</b> {event.venue}, {event.city}
                  </div>
                  <div className="event-el">
                    <b>Skala wydarzenia:</b> {event.min_people} -{" "}
                    {event.max_people} osób
                  </div>
                  {/* <div className="event-el">
                    <b>Dotyczy:</b> {categories[event.product]}
                  </div> */}
                  <div className="event-el">
                    <b>Położenie punktu sprzedaży:</b> (
                    {Math.round(event.latitude * 1000) / 1000},{" "}
                    {Math.round(event.longitude * 1000) / 1000})
                  </div>
                </div>
              ))
            : ""}
        </div>
      </div>
    </div>
  );
};

export default Analysis;
