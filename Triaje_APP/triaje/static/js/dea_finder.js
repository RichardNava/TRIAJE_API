window.navigator.geolocation.getCurrentPosition((position) => {
    console.log(position);
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    const lat = document.querySelector("#lat");
    const lng = document.querySelector("#lng");
    lat.value = latitude;
    lng.value = longitude;     
});
