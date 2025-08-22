document.addEventListener("DOMContentLoaded", function () {
    const yearSlider = document.getElementById('year-slider');

    // Dohvaćamo vrijednosti iz HTML input polja (koje postavlja Django)
    const minYear = parseInt(document.getElementById('min-year-input').value);
    const maxYear = parseInt(document.getElementById('max-year-input').value);

    // Kreiramo slider s dinamičkim rasponom
    noUiSlider.create(yearSlider, {
        start: [minYear, maxYear],
        connect: true,
        step: 1,
        range: {
            min: minYear,
            max: maxYear
        },
        tooltips: [true, true],
        format: {
            to: value => Math.round(value),
            from: value => Number(value)
        }
    });

    // Elementi za prikaz i unos godina
    const minYearInput = document.getElementById('min-year-input');
    const maxYearInput = document.getElementById('max-year-input');
    const minYearDisplay = document.getElementById('year-min');
    const maxYearDisplay = document.getElementById('year-max');

    // Povezivanje slidera s input poljima i prikazom
    yearSlider.noUiSlider.on('update', function (values) {
        minYearInput.value = values[0];
        maxYearInput.value = values[1];
        minYearDisplay.innerText = values[0];
        maxYearDisplay.innerText = values[1];
    });
});




