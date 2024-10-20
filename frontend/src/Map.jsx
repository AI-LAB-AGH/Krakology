import React, { useState } from "react";
import {
  GoogleMap,
  LoadScript,
  Marker,
  InfoWindow,
} from "@react-google-maps/api";
import "./index.css";

const Map = ({ locations }) => {
  const [selected, setSelected] = useState(null);
  const mapContainerStyle = {
    height: "500px",
    width: "100%",
  };

  return (
    <LoadScript googleMapsApiKey="AIzaSyDuNZvCLYEJEnx-vjvECR4H1ge-I6e7p8s">
      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        zoom={10}
        center={
          selected
            ? { lat: selected[0], lng: selected[1] }
            : { lat: 50.0647, lng: 19.945 }
        }
      >
        {locations
          ? locations.map((location) => (
              <Marker
                position={{
                  lat: location[0],
                  lng: location[1],
                }}
                onClick={() => setSelected(location)}
              />
            ))
          : ""}

        {selected && (
          <InfoWindow
            position={{ lat: selected[0], lng: selected[1] }}
            onCloseClick={() => setSelected(null)}
          >
            <div>{selected[2]}</div>
          </InfoWindow>
        )}
      </GoogleMap>
    </LoadScript>
  );
};

export default Map;
