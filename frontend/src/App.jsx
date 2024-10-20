import { useState } from "react";
import Analysis from "./Analysis";
import "./index.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploaded, setUploaded] = useState(false);

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
    await fetch("api/upload/", {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data) {
          setUploaded(true);
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
    <div className={"document" + (uploaded ? " full" : "")}>
      <div className="wrapper">
        <p className="upload-text">
          {selectedFile ? (
            <span>Wybrano:&nbsp;{selectedFile.name}</span>
          ) : (
            <span>
              Wybierz plik zawierający dane dotyczące
              sprzedaży.&nbsp;Akceptowany format to:&nbsp;.csv
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
            style={{ display: "none" }}
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
      <Analysis hide={!uploaded}></Analysis>
    </div>
  );
}

export default App;
