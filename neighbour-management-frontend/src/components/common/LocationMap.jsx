import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
} from "react-leaflet";

import L from "leaflet";


// ======================================================
// FIX LEAFLET DEFAULT MARKER ICON
// ======================================================

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({

  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",

  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",

  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",

});


// ======================================================
// LOCATION MAP COMPONENT
// ======================================================

function LocationMap({ location }) {

  // ====================================================
  // NO LOCATION SELECTED
  // ====================================================

  if (!location) {

    return (

      <div className="h-[350px] rounded-2xl border border-slate-200 bg-slate-50 flex flex-col items-center justify-center">

        <div className="text-4xl mb-3">
          📍
        </div>

        <p className="text-slate-600 font-semibold">
          Select a Jio Center
        </p>

        <p className="text-sm text-slate-400 mt-1">
          The selected JC location will appear here
        </p>

      </div>

    );

  }


  // ====================================================
  // MAP
  // ====================================================

  return (

    <div className="relative overflow-hidden rounded-2xl border border-slate-200">

      <MapContainer
        center={[
          location.latitude,
          location.longitude,
        ]}
        zoom={13}
        scrollWheelZoom={true}
        className="h-[350px] w-full"
      >

        {/* ================================================= */}
        {/* OPEN STREET MAP                                  */}
        {/* ================================================= */}

        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />


        {/* ================================================= */}
        {/* JC MARKER                                       */}
        {/* ================================================= */}

        <Marker
          position={[
            location.latitude,
            location.longitude,
          ]}
        >

          <Popup>

            <div className="min-w-[150px]">

              <p className="font-bold text-slate-800">
                {location.jc}
              </p>

              <p className="text-sm text-slate-500">
                {location.state}
              </p>

              <div className="mt-2 text-xs text-slate-400">

                Latitude:
                {" "}
                {location.latitude}

                <br />

                Longitude:
                {" "}
                {location.longitude}

              </div>

            </div>

          </Popup>

        </Marker>

      </MapContainer>


      {/* ================================================= */}
      {/* LOCATION INFORMATION                             */}
      {/* ================================================= */}

      <div className="absolute bottom-4 left-4 z-[1000] bg-white rounded-xl shadow-lg px-4 py-3">

        <p className="text-xs text-slate-500">
          Selected Jio Center
        </p>

        <p className="font-bold text-slate-800">
          {location.jc}
        </p>

        <p className="text-xs text-blue-600">
          {location.state}
        </p>

      </div>

    </div>

  );

}


export default LocationMap;