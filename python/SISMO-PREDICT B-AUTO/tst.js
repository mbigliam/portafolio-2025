function updateSkyLive() {
  fetch("/api/sky").then(function (r) { return r.json(); }).then(function (sky) {
    G.sats.clearLayers();
    MINI_SATS.clearLayers();

    (sky.satellites || []).forEach(function (s) {
      if (s.latitude == null || s.longitude == null) return;
      var la = +s.latitude, lo = +s.longitude;
      L.circleMarker([la, lo], { radius: 3, color: "#3aa0ff", fillColor: "#3aa0ff", fillOpacity: 0.9, weight: 1 })
        .bindTooltip("🛰️ " + s.name + "<br>Alt " + Math.round(s.altitude_km || 0) + " km").addTo(G.sats);
      L.circleMarker([la, lo], { radius: 2, color: "#3aa0ff", fillOpacity: 0.9, weight: 1 }).addTo(MINI_SATS);
    });

    if (sky.iss) {
      var la = +sky.iss.latitude, lo = +sky.iss.longitude;

      L.circleMarker([la, lo], { radius: 5, color: "#ff9f43", fillColor: "#ff9f43", fillOpacity: 1, weight: 2 })
        .bindTooltip("🛰️ ISS · " + Math.round(sky.iss.altitude_km || 0) + " km").addTo(G.sats);
      L.circleMarker([la, lo], { radius: 4, color: "#ff9f43", fillColor: "#ff9f43", fillOpacity: 1, weight: 2 }).addTo(MINI_SATS);

      if (issTrail.length && Math.abs(lo - issTrail[issTrail.length - 1][1]) > 180) issTrail = [];
      issTrail.push([la, lo]);
      if (issTrail.length > 400) issTrail.shift();
      if (issTrailLine) minimap.removeLayer(issTrailLine);
      issTrailLine = L.polyline(issTrail, { color: "#ff9f43", weight: 1, opacity: 0.8 }).addTo(minimap);

      var el = document.getElementById("iss_live");
      if (el) {
        el.innerHTML =
          '<div class="row"><span>Latitud</span><span class="badge blue">' + la.toFixed(2) + "°</span></div>" +
          '<div class="row"><span>Longitud</span><span class="badge blue">' + lo.toFixed(2) + "°</span></div>" +
          '<div class="row"><span>Altitud</span><span class="badge green">' + Math.round(sky.iss.altitude_km || 0) + " km</span></div>" +
          '<div class="row"><span>Velocidad</span><span class="badge green">' + Math.round(sky.iss.velocity_kmh || 0).toLocaleString() + " km/h</span></div>" +
          '<div class="row"><span>Visibilidad</span><span class="badge ' + (sky.iss.visibility === "daylight" ? "green" : "blue") + '">' + (sky.iss.visibility || "-") + "</span></div>";
        
      }
    }
  }).catch(function (e) { console.error("sky live:", e); });
}