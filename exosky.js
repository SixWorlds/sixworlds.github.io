const planetPicker = document.getElementById('planet-picker');
// planetPicker.attributes.setNamedItem('disabled');
let planets = null;
currentPlanet = '';

async function loadPlanets() {
  const planetsResponse = await fetch('https://sixworlds.github.io/assets/planets_demo.json');
  planets = await planetsResponse.json();
  
  Object.keys(planets)
    .sort((a,b) => a.localeCompare(b))
    .forEach((name) => {
      const option = document.createElement('option');
      option.value = name;
      option.innerText = name;
      planetPicker.appendChild(option);
    });
  
  switchSkyBox(Object.keys(planets)[0], 'skybox');
  currentPlanet = Object.keys(planets)[0];
  loading.style.display = 'none';
  document.getElementById('drag').style.display = 'block';
}

planetPicker.addEventListener('change', (e) => {
  const selectedPlanet = e.target.value;
  currentPlanet = selectedPlanet;
  switchSkyBox(selectedPlanet, 'skybox');
});

document.getElementById('skymap-n', () => {
  window.open(`https://sixworlds.github.io/assets/${currentPlanet}/skymap_n.png`, 'blank');
});

document.getElementById('skymap-s', () => {
  window.open(`https://sixworlds.github.io/assets/${currentPlanet}/skymap_s.png`, 'blank');
});

loadPlanets().then();
