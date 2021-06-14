window.navigator.geolocation.getCurrentPosition((position) => {
    console.log(position);
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    const lati = document.querySelector("#lati");
    const long = document.querySelector("#long");
    lati.value = latitude;
    long.value = longitude;     
});