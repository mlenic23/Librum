document.addEventListener("DOMContentLoaded", function () {
    const yearSlider = document.getElementById('year-slider');
    const minYear = parseInt(document.getElementById('min-year-input').value) || 1900;
    const maxYear = parseInt(document.getElementById('max-year-input').value) || 2025;

    noUiSlider.create(yearSlider, {
        start: [minYear, maxYear],
        connect: true,
        step: 1,
        range: {
            min: 1500,
            max: 2025
        },
        tooltips: [true, true], 
        format: {
            to: value => Math.round(value),
            from: value => Number(value)
        }
    });

    const minYearInput = document.getElementById('min-year-input');
    const maxYearInput = document.getElementById('max-year-input');
    const minYearDisplay = document.getElementById('year-min');
    const maxYearDisplay = document.getElementById('year-max');

    yearSlider.noUiSlider.on('update', function (values) {
        minYearInput.value = values[0];
        maxYearInput.value = values[1];
        minYearDisplay.innerText = values[0];
        maxYearDisplay.innerText = values[1];
    });
});