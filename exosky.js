const planetPicker = document.getElementById('planet-picker');
// planetPicker.attributes.setNamedItem('disabled');
let planets = null;

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
  
  loading.style.display = 'none';
}

planetPicker.addEventListener('change', (e) => {
  const selectedPlanet = e.target.value;
  switchSkyBox(selectedPlanet, 'skybox');
});

loadPlanets().then();
