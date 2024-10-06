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
  
  switchSkyBox(Object.keys(planets)[0], 'skybox');
  loading.style.display = 'none';
  document.getElementById('drag').style.display = 'block';
}

planetPicker.addEventListener('change', (e) => {
  const selectedPlanet = e.target.value;
  switchSkyBox(selectedPlanet, 'skybox');
});

loadPlanets().then();
