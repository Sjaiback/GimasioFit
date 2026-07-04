const startButton = document.querySelector("#start-scanner");
const video = document.querySelector("#qr-video");
const payloadInput = document.querySelector("#payload-input");
const scanForm = document.querySelector("#scan-form");

let scanning = false;

async function startScanner() {
  if (!("BarcodeDetector" in window)) {
    window.alert("Este navegador no soporta lector QR por camara. Usa el campo manual.");
    return;
  }

  const detector = new BarcodeDetector({ formats: ["qr_code"] });
  const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
  video.srcObject = stream;
  await video.play();
  scanning = true;

  async function tick() {
    if (!scanning) return;
    try {
      const codes = await detector.detect(video);
      if (codes.length > 0) {
        payloadInput.value = codes[0].rawValue;
        scanning = false;
        stream.getTracks().forEach((track) => track.stop());
        scanForm.requestSubmit();
        return;
      }
    } catch (error) {
      console.warn("No se pudo leer el QR", error);
    }
    window.requestAnimationFrame(tick);
  }

  tick();
}

if (startButton) {
  startButton.addEventListener("click", () => {
    startScanner().catch((error) => {
      window.alert(`No se pudo activar la camara: ${error.message}`);
    });
  });
}
