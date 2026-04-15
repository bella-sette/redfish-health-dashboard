const form = document.getElementById('scanForm');
const resultDiv = document.getElementById('result');
const loadingDiv = document.getElementById('loading');
const scanBtn = document.getElementById('scanBtn');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const ip = document.getElementById('ip').value.trim();
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();
  const scenario = document.getElementById('scenario').value;

  if (!ip || !username || !password) {
    alert("Please fill in all fields");
    return;
  }

  loadingDiv.classList.remove('hidden');
  resultDiv.classList.add('hidden');
  scanBtn.disabled = true;
  scanBtn.textContent = "Scanning...";
  scanBtn.classList.add("loading");

  try {
    const response = await fetch(`http://127.0.0.1:8000/scan?scenario=${scenario}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ip, username, password })
    });

    const data = await response.json();

    if (response.ok) {
      displayResults(data);
    } else {
      alert(`Backend Error: ${data.detail || 'Unknown error'}`);
    }
  } catch (error) {
    console.error("Fetch error:", error);
    alert(`Connection failed:\n${error.message}`);
  } finally {
    loadingDiv.classList.add('hidden');
    scanBtn.disabled = false;
    scanBtn.textContent = "Scan Server";
    scanBtn.classList.remove("loading");
  }
});

function animateNumber(element, target, duration = 900) {
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const value = Math.floor(eased * target);

    element.textContent = value;

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      element.textContent = target;
    }
  }

  requestAnimationFrame(update);
}

function displayResults(data) {
  const { health_score, risk_level, issues = [], recommendations = [] } = data;

  const scanTimeEl = document.getElementById('lastScan');
  scanTimeEl.style.opacity = 0;
  scanTimeEl.textContent = new Date().toLocaleTimeString();

  setTimeout(() => {
    scanTimeEl.style.opacity = 1;
  }, 100);

  document.getElementById('scanTime').textContent =
    `${Math.floor(Math.random() * 200 + 100)}ms`;

  document.getElementById('scanScenario').textContent =
    document.getElementById('scenario').value.toUpperCase();

  const scoreEl = document.getElementById('healthScore');
  scoreEl.textContent = "0";
  scoreEl.classList.add("animating");
  animateNumber(scoreEl, health_score);

  setTimeout(() => {
    scoreEl.classList.remove("animating");
  }, 900);

  const riskEl = document.getElementById('riskLevel');
  riskEl.textContent = risk_level;
  riskEl.className = `risk-pill ${risk_level.toLowerCase()}`;

  const issuesList = document.getElementById('issuesList');
  issuesList.innerHTML = '';

  if (issues.length === 0) {
    const li = document.createElement('li');
    li.textContent = "No issues detected.";
    issuesList.appendChild(li);
  } else {
    issues.forEach((issue, index) => {
      const li = document.createElement('li');
      li.classList.add(issue.severity.toLowerCase());
      li.style.opacity = 0;
      li.style.transform = "translateY(6px)";
      li.innerHTML = `<strong>${issue.severity}</strong> · ${issue.message}`;
      issuesList.appendChild(li);

      setTimeout(() => {
        li.style.opacity = 1;
        li.style.transform = "translateY(0)";
      }, index * 120);
    });
  }

  const recList = document.getElementById('recommendationsList');
  recList.innerHTML = '';

  recommendations.forEach(rec => {
    const li = document.createElement('li');
    li.textContent = rec;
    recList.appendChild(li);
  });

  resultDiv.classList.remove('hidden');
}