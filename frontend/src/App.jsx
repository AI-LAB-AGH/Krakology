import { useState } from "react";
import "./index.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [events, setEvents] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];
    setSelectedFile(file || null);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("csv", selectedFile);
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
    <>
      <div className="wrapper">
        <div className="upload-text">
          {events
            ? events.map((event) => (
                <>
                  <div className="bg-asseco-blue">{event.type}</div>
                  <div className="bg-hack-purple">{event.scale}</div>
                  <div>{event.start}</div>
                  <div>{event.end}</div>
                  <div>{event.location}</div>
                </>
              ))
            : ""}
        </div>

        <p className="upload-filename">
          {selectedFile ? (
            <span>Wybrano:&nbsp;{selectedFile.name}</span>
          ) : (
            <span>
              Wybierz plik zawierający dane dotyczące
              sprzedaży.&nbsp;Akceptowane formaty to:&nbsp;.csv,&nbsp;.xlsx
            </span>
          )}
        </p>

        <div className="upload-buttons">
          <label for="upload" className="button">
            Wybierz
          </label>
          <input
            id="upload"
            type="file"
            accept=".csv, .xlsx"
            required
            onChange={handleFileChange}
          />

          <button
            className="button"
            disabled={selectedFile ? false : true}
            onClick={handleUpload}
          >
            Analizuj
          </button>
        </div>
      </div>
    </>
  );
}

export default App;
